import pdfplumber


def extract_text_from_pdf(file_path):

    text = ""

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:
            text += page.extract_text() or ""

    return text


def extract_links_from_pdf(file_path):

    links = []

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            for link in page.hyperlinks:

                uri = link.get("uri")

                if uri:
                    links.append(uri)

    return links