import importlib.util
import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

SCRIPT = Path(r"C:\Users\EDY\.claude\skills\supir-slides\scripts\render_long_image.py")
spec = importlib.util.spec_from_file_location("render_long_image", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def png_bytes(color="#ffffff"):
    image = Image.new("RGB", (160, 240), color)
    output = io.BytesIO()
    image.save(output, "PNG")
    return output.getvalue()


class RenderLongImageTests(unittest.TestCase):
    def setUp(self):
        self.temp = Path(__file__).parent / ".tmp-render"
        self.temp.mkdir(exist_ok=True)
        self.style = self.temp / "style.jpg"
        self.content = self.temp / "content.jpg"
        Image.new("RGB", (100, 100), "#55bbdd").save(self.style)
        Image.new("RGB", (100, 100), "#55bb66").save(self.content)

    def test_canvas_size_is_exact(self):
        self.assertEqual(module.CANVAS_SIZE, (950, 3677))

    def test_prompt_locks_reference_roles_and_excludes_text(self):
        prompt = module.build_prompt("hero")
        self.assertIn("visual style only", prompt)
        self.assertIn("sole composition and licensed-asset source", prompt)
        self.assertIn("Do not draw any Chinese text", prompt)
        self.assertIn("cyclist", prompt)

    def test_gpt_request_contains_size_and_two_reference_images(self):
        response = {"choices": [{"message": {"content": "data:image/png;base64," + __import__("base64").b64encode(png_bytes()).decode()}}]}
        class FakeResponse:
            def __enter__(self): return self
            def __exit__(self, *_): pass
            def read(self): return json.dumps(response).encode()
        with patch.dict("os.environ", {"GPT_IMAGE_API_KEY": "test"}, clear=False), patch("urllib.request.urlopen", return_value=FakeResponse()) as mocked:
            result = module.generate_background("test", self.style, self.content, "1024x1536")
        self.assertEqual(result[:8], b"\x89PNG\r\n\x1a\n")
        payload = json.loads(mocked.call_args.args[0].data.decode())
        self.assertEqual(payload["model"], "gpt-image-2-plus")
        self.assertEqual(payload["size"], "1024x1536")
        content = payload["messages"][0]["content"]
        self.assertEqual(len([item for item in content if item["type"] == "image_url"]), 2)

    def test_http_401_does_not_retry(self):
        error = __import__("urllib.error").error.HTTPError("https://x", 401, "unauthorized", {}, io.BytesIO())
        with patch.dict("os.environ", {"GPT_IMAGE_API_KEY": "test"}, clear=False), patch("urllib.request.urlopen", side_effect=error) as mocked:
            with self.assertRaisesRegex(RuntimeError, "401"):
                module.generate_background("test", self.style, self.content, "1024x1536")
        self.assertEqual(mocked.call_count, 1)

    def test_composite_is_exact_png(self):
        backgrounds = {key: Image.open(io.BytesIO(png_bytes("#ddf5ee"))).convert("RGB") for key in ("hero", "mid", "footer")}
        canvas = module.build_canvas(backgrounds)
        output = self.temp / "result.png"
        canvas.save(output, "PNG")
        with Image.open(output) as image:
            self.assertEqual(image.size, (950, 3677))
            self.assertEqual(image.format, "PNG")


if __name__ == "__main__":
    unittest.main()
