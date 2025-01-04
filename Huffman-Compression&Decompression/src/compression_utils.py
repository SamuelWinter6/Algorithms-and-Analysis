import copy
from queue import *
from dataclasses import *
from typing import *
from byte_utils import *
import heapq

# [!] Important: This is the character code of the End Transmission Block (ETB)
# Character -- use this constant to signal the end of a message
ETB_CHAR = "\x17"

class HuffmanNode:
    '''
    HuffmanNode class to be used in construction of the Huffman Trie
    employed by the ReusableHuffman encoder/decoder below.
    '''
    
    # Educational Note: traditional constructor rather than dataclass because of need
    # to set default values for children parameters
    def __init__(self, char: Optional[str], freq: int, 
                 zero_child: Optional["HuffmanNode"] = None, 
                 one_child: Optional["HuffmanNode"] = None):
        '''
        HuffNodes represent nodes in the HuffmanTrie used to create a lossless
        encoding map used for compression. Their properties are given in this
        constructor's arguments:
        
        Parameters:
            char (str):
                Really, a single character, storing the character represented
                by a leaf node in the trie
            freq (int):
                The frequency with which the character / characters in a subtree
                appear in the corpus
            zero_child, one_child (Optional[HuffmanNode]):
                The children of any non-leaf, or None if a leaf; the zero_child
                will always pertain to the 0 bit part of the prefix, and vice
                versa for the one_child (which will add a 1 bit to the prefix)
        '''
        self.char = char
        self.freq = freq
        self.zero_child = zero_child
        self.one_child = one_child

class ReusableHuffman:
    '''
    ReusableHuffman encoder / decoder that is trained on some original
    corpus of text and can then be used to compress / decompress other
    text messages that have similar distributions of characters.
    '''
    
    def __init__(self, corpus: str):
        '''
        Constructor for a new ReusableHuffman encoder / decoder that is fit to
        the given text corpus and can then be used to compress and decompress
        messages with a similar distribution of characters.
        
        Parameters:
            corpus (str):
                The text corpus on which to fit the ReusableHuffman instance,
                which will be used to construct the encoding map
        '''
        self._encoding_map: dict[str, str] = dict()
        
        # [!] TODO: complete construction of self._encoding_map by constructing
        # the Huffman Trie -- remember to save its root as an attribute!
        # >> [BAC] Remove print statements before submission in the future; they will substantially
        # slow your solution down! (-0.5)
        print('\n\nCorpus:', corpus)

        def node_less_than(self: 'HuffmanNode', other: 'HuffmanNode') -> bool:
            '''
            Determines if this Huffman node has a lower frequency than another node.

            This method is used for comparing two Huffman nodes, primarily during the
            construction of the Huffman tree where nodes are sorted based on their frequency.
            Nodes with lower frequencies have higher priority in the queue.

            Parameters:
                self (HuffmanNode): The current instance of HuffmanNode.
                other (HuffmanNode): Another instance of HuffmanNode to compare against.

            Returns:
                bool: True if this node's frequency is less than the other node's frequency, False otherwise.
            '''
            # >> [BAC] Ah whoops -- here's a problem: remember that nodes are prioritized by frequency first
            # but then with ties broken by their character field. What happens if you give all non-leaves
            # the same character? Review the tiebreaking criteria, which is earliest character *in a subtree*
            return self.freq < other.freq

        def node_is_leaf(self: 'HuffmanNode') -> bool:
            '''
            Checks if this Huffman node is a leaf node.

            Leaf nodes in a Huffman tree do not have child nodes and represent individual
            characters in the encoding scheme. This method helps identify such nodes, which
            is crucial for the encoding and decoding processes.

            Parameters:
                self (HuffmanNode): The current instance of HuffmanNode.

            Returns:
                bool: True if this node is a leaf node (i.e., has no children), False otherwise.
            '''
            return self.zero_child is None and self.one_child is None
        
        setattr(HuffmanNode, '__lt__', node_less_than)
        setattr(HuffmanNode, 'is_leaf', node_is_leaf)
        
        frequencies = {char: corpus.count(char) for char in set(corpus)}
        frequencies[ETB_CHAR] = frequencies.get(ETB_CHAR, 0) + 1

        priority_queue: List = []

        for char, freq in frequencies.items():
            heapq.heappush(priority_queue, (freq, char, HuffmanNode(char, freq)))

        while len(priority_queue) > 1:
            freq1, char1, zero_child = heapq.heappop(priority_queue)
            freq2, char2, one_child = heapq.heappop(priority_queue)
            earliest_char = min(char1, char2) if char1 != '\uffff' and char2 != '\uffff' else (char1 if char1 != '\uffff' else char2)
            merged_node = HuffmanNode(None, freq1 + freq2, zero_child, one_child)
            heapq.heappush(priority_queue, (merged_node.freq, earliest_char, merged_node))

        self.huffman_tree_root = heapq.heappop(priority_queue)[2]

        def generate_encoding_map(node: Optional[HuffmanNode], path: str = "") -> None:
            '''
            Recursively generates the encoding map from the Huffman tree.
            
            Parameters:
                node: Optional[HuffmanNode] - Current node in the Huffman tree.
                path: str - Current bit string path to the node.
            '''
            if node is None:
                return
            if node.char is not None:
                self._encoding_map[node.char] = path
            else:
                generate_encoding_map(node.zero_child, path + "0")
                generate_encoding_map(node.one_child, path + "1")

        self._encoding_map = {}
        generate_encoding_map(self.huffman_tree_root)
        print("Encoding Map:", self._encoding_map)
    
    def get_encoding_map(self) -> dict[str, str]:
        '''
        Simple getter for the encoding map that, after the constructor is run,
        will be a dictionary of character keys mapping to their compressed
        bitstrings in this ReusableHuffman instance's encoding
        
        Example:
            {ETB_CHAR: 10, "A": 11, "B": 0}
            (see unit tests for more examples)
        
        Returns:
            dict[str, str]:
                A copy of this ReusableHuffman instance's encoding map
        '''
        return copy.deepcopy(self._encoding_map)
    
    # Compression
    # ---------------------------------------------------------------------------
    
    def compress_message(self, message: str) -> bytes:
        '''
        Compresses the given String message / text corpus into its Huffman-coded
        bitstring, and then converted into a Python bytes type.
        
        [!] Uses the _encoding_map attribute generated during construction.
        
        Parameters:
            message (str):
                String representing the corpus to compress
        
        Returns:
            bytes:
                Bytes storing the compressed corpus with the Huffman coded
                bytecode. Formatted as (1) the compressed message bytes themselves,
                (2) terminated by the ETB_CHAR, and (3) [Optional] padding of 0
                bits to ensure the final byte is 8 bits total.
        
        Example:
            huff_coder = ReusableHuffman("ABBBCC")
            compressed_message = huff_coder.compress_message("ABBBCC")
            # [!] Only first 5 bits of byte 1 are meaningful (rest are padding)
            # byte 0: 1010 0011 (100 = ETB, 101 = 'A', 0 = 'B', 11 = 'C')
            # byte 1: 1110 0000
            solution = bitstrings_to_bytes(['10100011', '11100000'])
            self.assertEqual(solution, compressed_message)
        '''
        # [!] TODO: Complete compression!
        # >> [BAC] I like that you tried something homespun here, but looks like you might've overlooked
        # the spec's byte_utils.py helpers that gives you the methods needed to do this conversion
        # in one line!
        bitstring = ''.join(self._encoding_map.get(char, '') for char in message)
        
        bitstring += self._encoding_map[ETB_CHAR]
        
        padding_length = (8 - len(bitstring) % 8) % 8
        bitstring += '0' * padding_length
        
        byte_array = bytearray()
        for i in range(0, len(bitstring), 8):
            byte = int(bitstring[i:i+8], 2)
            byte_array.append(byte)
        return bytes(byte_array)
    
    # Decompression
    # ---------------------------------------------------------------------------
    
    def decompress (self, compressed_msg: bytes) -> str:
        '''
        Decompresses the given bytes representing a compressed corpus into their
        original character format.
        
        [!] Should use the Huffman Trie generated during construction.
        
        Parameters:
            compressed_msg (bytes):
                Formatted as (1) the compressed message bytes themselves,
                (2) terminated by the ETB_CHAR, and (3) [Optional] padding of 0
                bits to ensure the final byte is 8 bits total.
        
        Returns:
            str:
                The decompressed message as a string.
        
        Example:
            huff_coder = ReusableHuffman("ABBBCC")
            # byte 0: 1010 0011 (100 = ETB, 101 = 'A', 0 = 'B', 11 = 'C')
            # byte 1: 1110 0000
            # [!] Only first 5 bits of byte 1 are meaningful (rest are padding)
            compressed_msg: bytes = bitstrings_to_bytes(['10100011', '11100000'])
            self.assertEqual("ABBBCC", huff_coder.decompress(compressed_msg))
        '''
        # [!] TODO: Complete decompression!

        bitstring = ''.join(f'{byte:08b}' for byte in compressed_msg)

        decoded_message = ''
        current_node = self.huffman_tree_root

        for bit in bitstring:
            current_node = current_node.zero_child if bit == '0' else current_node.one_child

            if current_node.is_leaf():
                if current_node.char == ETB_CHAR:
                    break  
                decoded_message += current_node.char
                current_node = self.huffman_tree_root

        return decoded_message
# ===================================================
# >>> [BAC] Summary
# Excellent submission that has a ton to like and was
# obviously well-tested. Good delegation of labor into
# helper methods, generally clean style, and shows
# strong command of programming foundations alongside
# data structure and algorithmic concepts. Keep up
# the great work! Just make sure you follow all of the 
# tie breaking criteria.
# ---------------------------------------------------
# >>> [BAC] Style Checklist
# [X] = Good, [~] = Mixed bag, [ ] = Needs improvement
# 
# [X] Variables and helper methods named and used well
# [X] Proper and consistent indentation and spacing
# [X] Proper JavaDocs provided for ALL methods
# [X] Logic is adequately simplified
# [X] Code repetition is kept to a minimum
# ---------------------------------------------------
# Correctness:       97.0 / 100 (-1.5 / missed test)
# Style Penalty:      -0.5
# Mypy Compliance:    -0.0       (-5 if mypy unhappy)
# Total:             96.5 / 100
# ===================================================