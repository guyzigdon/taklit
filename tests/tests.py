from image_detector import ImageDetector

# test ImageDetector.detect_image

def test_ImageDetector_detect_image():
    image_data = open("Dark_Side_of_the_Moon.jpg", "rb").read()
    result = ImageDetector().detect_image(image_data)

    import pdb; pdb.set_trace()
    assert result == VinylInformation.from_raw_information("raw_information")

test_ImageDetector_detect_image()