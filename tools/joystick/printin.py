from cereal import messaging
from uuid import uuid4
from cereal.visionipc import VisionIpcClient, VisionStreamType
from system.camerad.snapshot.snapshot import extract_image, jpeg_write
from common.params import Params

pm = messaging.PubMaster(['bodyStatus'])
vipc_client = VisionIpcClient("camerad", VisionStreamType.VISION_STREAM_DRIVER, True)


def send_body_status(res):
  msg = messaging.new_message()
  msg.bodyStatus = res
  pm.send('bodyStatus', msg)

def take_snapshot(filename):
  img = vipc_client.recv()
  img = extract_image(img.flatten(), vipc_client.width, vipc_client.height, vipc_client.stride, vipc_client.uv_offset)
  jpeg_write(filename, img)

def print_snapshot(filename):
  printer_ip = os.environ["PRINTER_ADDR"]
  os.system(f"ipptool -tv -f {filename} {printer_ip} /data/openpilot/tools/joystick/printjob.ipp")

def main():
  params = Params()
  while True:
    m = params.get_bool("TakePic", block=True)
    if not m:
      continue

    send_body_status(1)
    time.sleep(6)
    send_body_status(0)

    fname = f"/data/openpilot/{str(uuid4())}.jpeg"
    take_snapshot(fname)
    print_snapshot(fname)

    time.sleep(5)

    params.remove("TakePic")


if __name__=="__main__":
  main()
