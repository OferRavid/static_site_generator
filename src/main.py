from textnode import TextNode
from inline_markdown import extract_markdown_images, extract_markdown_links

def main():
    # text_node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    # print(text_node)
    # text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
    # print(extract_markdown_images(text))
    # # [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
    # text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
    # print(extract_markdown_links(text))
    # # [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
    print(list([1])[1])


if __name__ == "__main__":
    main()

