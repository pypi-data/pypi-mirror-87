import json
import logging
import math
import os
import re
import sys
import traceback

import fitz

"""
assumptions:
(1) most pages should have a page number (arabic number) printed in header or footer.
(2) the page numbers might not start from 1, but should be in ascending order.
"""

class PageNumberExtractor:

    class TextLineObj(object):
        """ class to represent a line of text in pdf """
        def __init__(self, text, bbox):
            self.text = text
            self.bbox = bbox

        def __repr__(self):
            result = { "Text": self.text, "Bbox": self.bbox }
            return json.dumps(result)

    def __init__(self, log_level=None):
        if log_level is None:
            log_level = logging.INFO
        logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)
        self.logger = logging.getLogger(__name__)

    def process(self, input_pdf):
        """
        Entry method of the class
        Return a dictionary of logical page number to physical ones (aka. the # printed on page).
        e.g., { 0:15, 1:16, 2:17, ..., 9:24 }
        """

        max_line_levels = 5
        total_pages, cand_lines_by_level, cand_lines_by_page = self.get_candidate_lines(input_pdf, max_line_levels)
        
        # note: total_pages can be more than len(cand_lines_by_page)
        # because we check no more than 20 pages
        longest_pairs = {}
        max_len = 0

        for line_level in range(0, max_line_levels):
            # level-by-level detect page numbers by checking each page's line counted from top/bottom
            pairs = self.find_page_numbers(cand_lines_by_level[line_level])
            if len(pairs) > max_len:
                longest_pairs = pairs
                max_len = len(pairs)

        # try put all lines in each page together, this may return a different sequence

        pairs = self.find_page_numbers(cand_lines_by_page)
        
        if len(pairs) > max_len:
            longest_pairs = pairs

        logical_pg_numbers = range(0, total_pages)
        result = self.fill_gaps(longest_pairs, logical_pg_numbers)

        return result

    def get_candidate_lines(self, input_pdf, max_line_levels=5, max_pages_to_check=20):
        """
        Given the pdf, return the header/footer lines that likely contain page numbers.
        Here use PyMuPdf to read pdf. Other pdf libraries can be used too.
        By default, pages_to_check = 20, don't have to check all pages to find a pattern.
        """
        pdf_doc = fitz.open(input_pdf)

        total_pages = pdf_doc.pageCount

        cand_lines_by_level = {}  # dictionary of dictionaries: line-level k ==> { pgn ==> text of the k-th line }
        for i in range(0, max_line_levels*2):
            cand_lines_by_level[i] = {}   # initialize a dictionary for each line level

        cand_lines_by_page = {}   # dictionary of pgn ==> all selected lines text in the page

        try:
            for pgn, page in enumerate(pdf_doc):
                if pgn >= max_pages_to_check:
                    break

                pg_dict = page.getText("dict")

                lines = self.get_text_lines_in_page(pg_dict)

                # add candidate lines to check for this page
                selected_lines = []
                n = len(lines)
                if n <= max_line_levels:
                    for i in range(0, n):
                        cand_lines_by_level[i][pgn] = lines[i].text
                        selected_lines.append(lines[i].text)
                elif n >= max_line_levels:
                    # add lines from page top
                    i = 0
                    while i < max_line_levels:
                        cand_lines_by_level[i][pgn] = lines[i].text
                        selected_lines.append(lines[i].text)
                        i += 1

                    # add lines from page bottom
                    i = 0
                    while i < max_line_levels:
                        cand_lines_by_level[max_line_levels + i][pgn] = lines[n-1-i].text  
                        selected_lines.append(lines[n-1-i].text)
                        i += 1

                cand_lines_by_page[pgn] = "\n".join(selected_lines)

        except Exception as ex:
            self.logger.debug("get_candidate_lines() - Exception: {}".format(ex))
            traceback.print_exc()
        finally:
            pdf_doc.close()

        return total_pages, cand_lines_by_level, cand_lines_by_page

    def get_text_lines_in_page(self, page_dict):
        pieces = []
        for block in page_dict["blocks"]:
            if block["type"] != 0:  # 0 means it's text line, type=1 is image block
                continue
            for line in block["lines"]:
                bbox = self.get_rounded_bbox(line["bbox"])
                text_spans = []
                for span in line["spans"]:
                    if len(span["text"]) > 0:
                        text_spans.append(span["text"])
                text = " ".join(text_spans).strip()
                if len(text) > 0:  # ignore empty lines
                    pieces.append(self.TextLineObj(text, bbox))

        # order the lines in up-down then left-right order
        sorted_pieces = sorted(pieces, key=lambda x: (x.bbox[1], x.bbox[0]))

        merged_lines = self.merge_pieces_in_same_line(sorted_pieces)

        return merged_lines

    def get_rounded_bbox(self, bbox):
        return [round(bbox[0]), round(bbox[1]), round(bbox[2]), round(bbox[3])]

    def merge_pieces_in_same_line(self, sorted_pieces):
        result = []
        if len(sorted_pieces) > 0:
            pieces_in_line = []
            i = 0
            prev_y = -1
            curr_y = -1
            while i < len(sorted_pieces):
                curr_piece = sorted_pieces[i]
                curr_y = curr_piece.bbox[1]
                if curr_y != prev_y and len(pieces_in_line) > 0:
                    # a new line
                    merged_pieces = self.merge_piece(pieces_in_line)
                    result.append(merged_pieces)
                    pieces_in_line = []

                pieces_in_line.append(curr_piece)
                prev_y = curr_y
                i += 1

            # handle the last piece
            pieces_in_line.append(curr_piece)
            merged_pieces = self.merge_piece(pieces_in_line)
            result.append(merged_pieces)
        return result

    def merge_piece(self, pieces):
        text_list = []
        bbox_list = []
        for piece in pieces:
            text_list.append(piece.text)
            bbox_list.append(piece.bbox)
        merged_text = " ".join(text_list).strip()
        merged_bbox = self.merge_bboxes(bbox_list)
        return self.TextLineObj(merged_text, merged_bbox)

    def merge_bboxes(self, boxes):
        if len(boxes) != 4:
            return []

        x1, y1, x2, y2 = boxes[0]
        for i in range(1, len(boxes)):
            x1 = min(x1, boxes[i][0])
            y1 = min(y1, boxes[i][1])
            x2 = max(x2, boxes[i][2])
            y2 = max(y2, boxes[i][3])
        return [x1, y1, x2, y2]

    def can_be_valid_pair(self, num_set1, num_set2, max_diff):
        """
        check if exists a pair (n1, n2), where n1 from num_set1, n2 from num_set2, satisfying:
        (1) n1 < n2
        (2) n2 - n1 <= max_diff
        """
        result = False
        if len(num_set1) > 0 and len(num_set2) > 0:
            for i in num_set1:
                for j in num_set2:
                    if i < j and j-i <=max_diff:
                        return True
        return result

    def find_page_numbers(self, cand_lines_by_page):
        """
        Return a dictionary mapping logical page # to physical ones.
        e.g., {0: 11, 1: 12, 2: 13, 3: 14, 4: 15, 5: 16, 6: 17}
        """

        total_logical_pages = len(cand_lines_by_page)

        # step 1: assume each line is a line from a page
        # a page number suppose to be unique to the correspoding page
        # for a seen number, here to find which pages it appears in
        physical_to_logical_mapping = {}  # physical pgn ==> a set of logical pgn
        logical_to_physical_mapping = {}  # logical pgn ==> a sorted list of physical pgn
        for pgn, line_text in cand_lines_by_page.items():
            physical_numbers = re.findall(r"\d+", line_text)
            physical_pgn_list = []
            if physical_numbers:
                # all physical numbers in this line
                for num_str in physical_numbers:
                    num = int(num_str)
                    physical_pgn_list.append(num)
                    if num in physical_to_logical_mapping.keys():
                        physical_to_logical_mapping[num].add(pgn)
                    else:
                        physical_to_logical_mapping[num] = {pgn}

            logical_to_physical_mapping[pgn] = sorted(physical_pgn_list)

        self.logger.debug("logical_to_physical_mapping:")
        self.logger.debug(logical_to_physical_mapping)

        self.logger.debug("physical_to_logical_mapping:")
        self.logger.debug(physical_to_logical_mapping)

        # step 2: the numbers appearing in only 1 page is likely the page number,
        # because a page number has to be unique across the pages (they should not appear more than once)
        # to allow some resilence to noices, a real page number might happen to occur more than once
        uniq_numbers = []
        max_occur = 3
        for num, pg_list in physical_to_logical_mapping.items():
            if len(pg_list) <= max_occur:
                uniq_numbers.append(num)

        self.logger.debug("len(uniq_numbers) = " + str(len(uniq_numbers)))

        # step 3: sort the "unique" numbers so that they are in ascending order
        uniq_numbers.sort()

        self.logger.debug("sorted uniq_numbers:")
        self.logger.debug(uniq_numbers)

        # step 4: find all candidate intervals that are roughly continuous and increasing
        cand_sequences = []
        i = 0
        j = 0
        n = len(uniq_numbers)
        min_len = max(3, round(total_logical_pages * 0.6))  # should cover >60% pages
        max_diff = 3  # diff btw two consecutive numbers should be no more than 3
        while i < n:
            j = i+1
            while j<n and uniq_numbers[j] - uniq_numbers[j-1] <= max_diff \
                and self.can_be_valid_pair(
                    physical_to_logical_mapping[uniq_numbers[j-1]],  # logical pg number set1
                    physical_to_logical_mapping[uniq_numbers[j]],    # logical pg number set2
                    max_diff
                ):
                j += 1

            if (j-i) > min_len:
                cand_sequences.append(uniq_numbers[i:j]) 

            i = j

        self.logger.debug("cand_sequences:")
        self.logger.debug(cand_sequences)

        # step 5: from the candidate sequence, pick the one whose sum-diff 
        # (sum of diff of current pgn - previous pgn) is closest to the total logical pages. 
        # e.g., if the pdf has 9 pages, then the sum-diff should ideally be 9-1 = 8.
        # if tie, pick the longer sequence (i.e., the one that covers more pages)
        closest_seq = []
        min_dist = 99999
        for seq in cand_sequences:
            sum_diff = seq[-1] - seq[0]
            dist = abs(sum_diff - total_logical_pages)
            if dist < min_dist:
                closest_seq = seq
                min_dist = dist
            elif dist == min_dist:
                # on tie, pick the one has smaller starting page#
                if seq[0] < closest_seq[0]:
                    closest_seq = seq
        
        self.logger.debug("closest_seq:")
        self.logger.debug(closest_seq)

        # step 6: turn list to dictionary
        pgn_pairs = {}

        prev_num = -1
        for pgn, physical_pgn_list in logical_to_physical_mapping.items():
            for num in closest_seq:
                if num in physical_pgn_list and num > prev_num:
                    pgn_pairs[pgn] = num
                    prev_num = num
                    break

        self.logger.debug("pgn_pairs:")
        self.logger.debug(pgn_pairs)

        return pgn_pairs

    def fill_gaps(self, cand_pairs, logical_pg_numbers):
        # go through the logical numbers, and fill the gap if any
        if len(cand_pairs) == 0:
            return {}

        n = len(logical_pg_numbers)
        unfilled_pgn = -1
        result = [unfilled_pgn] * n
        for pgn in logical_pg_numbers:
            if pgn in cand_pairs.keys():
                result[pgn] = cand_pairs[pgn]

        i = 0
        j = 0
        while i < n:
            while i<n and result[i] != -1:
                i += 1

            j = i+1
            while j<n and result[j] == -1:
                j += 1

            # set pgn from page i (inclusive) to j (exclusive)
            if (i>0):
                k = i
                while k < min(j, n):
                    result[k] = result[k-1] + 1
                    k += 1
            elif (j<n):
                k = j-1
                while k >= i:
                    result[k] = result[k+1] - 1
                    k -= 1

            i = j

        return { idx : val for idx, val in enumerate(result) }

if __name__ == "__main__":
    CUR_DIR = os.path.dirname(os.path.realpath(__file__))

    #pdf_file = sys.argv[1]
    pdf_file = CUR_DIR + os.path.sep + r"..\tests\sample-pdfs\2-col-pubmed-2.pdf" # 

    print("pdf_file: " + pdf_file)

    extractor = PageNumberExtractor(logging.DEBUG)
    page_numbers = extractor.process(pdf_file)

    print("\nresult:")
    print(page_numbers)