import io
import cv2
import os
import numpy as np


def detect_handwritten_ocr(path, service_account_json_file):
    """Detects handwritten characters in a local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision_v1p3beta1 as vision
    client = vision.ImageAnnotatorClient.from_service_account_json(service_account_json_file)

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    # Language hint codes for handwritten OCR:
    # en-t-i0-handwrit, mul-Latn-t-i0-handwrit
    # Note: Use only one language hint code per request for handwritten OCR.
    image_context = vision.types.ImageContext(
        language_hints=['en-t-i0-handwrit'])

    response = client.document_text_detection(image=image,
                                              image_context=image_context)

    # print('Full Text: {}'.format(response.full_text_annotation.text))
    # for page in response.full_text_annotation.pages:
    #     for block in page.blocks:
    #         print('\nBlock confidence: {}\n'.format(block.confidence))
    #
    #         for paragraph in block.paragraphs:
    #             print('Paragraph confidence: {}'.format(
    #                 paragraph.confidence))
    #
    #             for word in paragraph.words:
    #                 word_text = ''.join([
    #                     symbol.text for symbol in word.symbols
    #                 ])
    #                 print('Word text: {} (confidence: {})'.format(
    #                     word_text, word.confidence))
    #
    #                 for symbol in word.symbols:
    #                     print('\tSymbol: {} (confidence: {})'.format(
    #                         symbol.text, symbol.confidence))

    return response.full_text_annotation.text


def write_img(img, filename):
    filename = "{}.png".format(filename)
    cv2.imwrite(filename, img)
    return filename


def get_text_from_image(service_account_path, image_arg, preprocess_arg="none"):
    nparr = np.fromstring(image_arg, np.uint8)
    if len(nparr) == 0:
        raise Exception("Empty image!!")

    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = None

    # check to see if we should apply thresholding to preprocess the
    # image
    if preprocess_arg == "thresh":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 3)
        gray = cv2.adaptiveThreshold(blur, 255,
                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 11, 6)

        # gray = cv2.threshold(blur, 0, 255,
        #                      cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # make a check to see if median blurring should be done to remove
    # noise
    elif preprocess_arg == "blur":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
    elif preprocess_arg == "none":
        gray = image

    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = write_img(gray, "final")

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    text = detect_handwritten_ocr(filename, service_account_path)

    return text

