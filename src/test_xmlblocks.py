import unittest
from xmlblocks import markdown_to_blocks, block_to_block_type, BlockType

class TestXmlBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_2(self):
        md = """
        This is **bolded** paragraph

 This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line         

     




- This is a list
- with items



"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_head1(self):
        block_text = "# heading 1"
        block_type = block_to_block_type(block_text)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_head2(self):
        block_text = "## heading 2"
        block_type = block_to_block_type(block_text)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_head3(self):
        block_text = "### heading 3"
        block_type = block_to_block_type(block_text)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_head4(self):
        block_text = "#### heading 4"
        block_type = block_to_block_type(block_text)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_head5(self):
        block_text = "##### heading 5"
        block_type = block_to_block_type(block_text)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_head6(self):
        block_text = "###### heading 6"
        block_type = block_to_block_type(block_text)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_head7_fail(self):
        block_text = "####### heading 7"
        block_type = block_to_block_type(block_text)
        self.assertNotEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_head_space_fail(self):
        block_text = "######heading 6"
        block_type = block_to_block_type(block_text)
        self.assertNotEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_head_start_fail(self):
        block_text = "oh hey heres a ##### heading 5"
        block_type = block_to_block_type(block_text)
        self.assertNotEqual(block_type, BlockType.HEADING)

    
    def test_block_to_block_type_code_single(self):
        block_text = '''```
here is some code block nonsense
```'''
        block_type = block_to_block_type(block_text)
        self.assertEqual(block_type, BlockType.CODE)
    
    def test_block_to_block_type_code_multi(self):
        block_text = '''```
here is some code block nonsense
and some more
and a bit more
    heck we can even add some leading tabs
```'''
        block_type = block_to_block_type(block_text)
        self.assertEqual(block_type, BlockType.CODE)
    
    def test_block_to_block_type_code_fail_leading(self):
        block_text = '''
        ```
here is some code block nonsense
and some more
and a bit more
    heck we can even add some leading tabs
```'''
        block_type = block_to_block_type(block_text)
        self.assertNotEqual(block_type, BlockType.CODE)
    
    def test_block_to_block_type_code_fail_trailing(self):
        block_text = '''```
here is some code block nonsense
and some more
and a bit more
    heck we can even add some leading tabs
```
nosense'''
        block_type = block_to_block_type(block_text)
        self.assertNotEqual(block_type, BlockType.CODE)

    
    def test_block_to_block_type_quote_single(self):
        block_text = '''> here is a quote line'''
        block_type = block_to_block_type(block_text)
        self.assertEqual(block_type, BlockType.QUOTE)
    
    def test_block_to_block_type_quote_multi(self):
        block_text = '''> here is a quote line
> and another
> and even more'''
        block_type = block_to_block_type(block_text)
        self.assertEqual(block_type, BlockType.QUOTE)
    
    def test_block_to_block_type_quote_multi_nospace(self):
        block_text = '''> here is a quote line
>and another
> and even more'''
        block_type = block_to_block_type(block_text)
        self.assertEqual(block_type, BlockType.QUOTE)
    
    def test_block_to_block_type_quote_fail_leading(self):
        block_text = '''this > here is a quote line
> and another
> and even more'''
        block_type = block_to_block_type(block_text)
        self.assertNotEqual(block_type, BlockType.QUOTE)
    
    def test_block_to_block_type_quote_fail_trailing(self):
        block_text = '''> here is a quote line
> and another
> and even more

but this is not right'''
        block_type = block_to_block_type(block_text)
        self.assertNotEqual(block_type, BlockType.QUOTE)
    
    def test_block_to_block_type_quote_fail_middle(self):
        block_text = '''> here is a quote line
and another wrong
> and even more'''
        block_type = block_to_block_type(block_text)
        self.assertNotEqual(block_type, BlockType.QUOTE)
    
    def test_block_to_block_type_quote_fail_leading_mid(self):
        block_text = '''> here is a quote line
  > and another wrong
> and even more'''
        block_type = block_to_block_type(block_text)
        self.assertNotEqual(block_type, BlockType.QUOTE)

    
    def test_block_to_block_type_ul_single(self):
        block_text = '''- an unordered list?'''
        block_type = block_to_block_type(block_text)
        self.assertEqual(block_type, BlockType.U_LIST)
    
    def test_block_to_block_type_ul_multi(self):
        block_text = '''- an unordered list?
- an unordered list? again
- an unordered list so many lines'''
        block_type = block_to_block_type(block_text)
        self.assertEqual(block_type, BlockType.U_LIST)
    
    def test_block_to_block_type_ul_fail_leading(self):
        block_text = ''' - an unordered list?'''
        block_type = block_to_block_type(block_text)
        self.assertNotEqual(block_type, BlockType.U_LIST)
    
    def test_block_to_block_type_ul_fail_nospace(self):
        block_text = '''- an unordered list?
-no spaces?
- this is fine tho'''
        block_type = block_to_block_type(block_text)
        self.assertNotEqual(block_type, BlockType.U_LIST)
    
    def test_block_to_block_type_ul_fail_wrong_line(self):
        block_text = '''- an unordered list?
 - no spaces?
- this is fine tho'''
        block_type = block_to_block_type(block_text)
        self.assertNotEqual(block_type, BlockType.U_LIST)
    
    def test_block_to_block_type_ul_fail_missing(self):
        block_text = '''- an unordered list?
no spaces?
- this is fine tho'''
        block_type = block_to_block_type(block_text)
        self.assertNotEqual(block_type, BlockType.U_LIST)

    
    def test_block_to_block_type_ol_single(self):
        block_text = '''1. an unordered list?'''
        block_type = block_to_block_type(block_text)
        self.assertEqual(block_type, BlockType.O_LIST)
    
    def test_block_to_block_type_ol_multi(self):
        block_text = '''1. an unordered list?
2. an unordered list? again
3. an unordered list so many lines'''
        block_type = block_to_block_type(block_text)
        self.assertEqual(block_type, BlockType.O_LIST)
    
    def test_block_to_block_type_ol_multi_long(self):
        block_text = '''1. an unordered list?
2. an unordered list? again
3. an unordered list so many lines
4. an unordered list so many lines
5. an unordered list so many lines
6. an unordered list so many lines
7. an unordered list so many lines
8. an unordered list so many lines
9. an unordered list so many lines
10. an unordered list so many lines
11. an unordered list so many lines
12. an unordered list so many lines
13. an unordered list so many lines'''
        block_type = block_to_block_type(block_text)
        self.assertEqual(block_type, BlockType.O_LIST)
    
    def test_block_to_block_type_ol_fail_leading(self):
        block_text = ''' 1. an unordered list?'''
        block_type = block_to_block_type(block_text)
        self.assertNotEqual(block_type, BlockType.O_LIST)
    
    def test_block_to_block_type_ol_fail_nospace(self):
        block_text = '''1. an unordered list?
2.no spaces?
3. this is fine tho'''
        block_type = block_to_block_type(block_text)
        self.assertNotEqual(block_type, BlockType.O_LIST)
    
    def test_block_to_block_type_ol_fail_wrong_line(self):
        block_text = '''1. an unordered list?
 2. no spaces?
3. this is fine tho'''
        block_type = block_to_block_type(block_text)
        self.assertNotEqual(block_type, BlockType.O_LIST)
    
    def test_block_to_block_type_ol_fail_missing(self):
        block_text = '''1. an unordered list?
no spaces?
2. this is fine tho'''
        block_type = block_to_block_type(block_text)
        self.assertNotEqual(block_type, BlockType.O_LIST)
    
    def test_block_to_block_type_ol_fail_order(self):
        block_text = '''1. an unordered list?
3. no spaces?
2. this is fine tho'''
        block_type = block_to_block_type(block_text)
        self.assertNotEqual(block_type, BlockType.O_LIST)
    
    def test_block_to_block_type_ol_fail_duplicates(self):
        block_text = '''1. an unordered list?
1. no spaces?
2. this is fine tho'''
        block_type = block_to_block_type(block_text)
        self.assertNotEqual(block_type, BlockType.O_LIST)
    
    def test_block_to_block_type_ol_fail_bad_start(self):
        block_text = '''3. an unordered list?
4. no spaces?
5. this is fine tho'''
        block_type = block_to_block_type(block_text)
        self.assertNotEqual(block_type, BlockType.O_LIST)


if __name__ == "__main__":
    unittest.main()