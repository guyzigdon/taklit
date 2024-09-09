from image_detector import ImageDetector

# test ImageDetector.detect_image

def test_detect_image():
    image_data = open("tests/Dark_Side_of_the_Moon.jpg", "rb").read()
    import pdb; pdb.set_trace()
    result = ImageDetector().detect_image(image_data)

    assert result == VinylInformation.from_raw_information("raw_information")

test_detect_image()