import argparse
import logging

from getmac import get_mac_address

from metzctl import MetzRemote
from metzctl.remote import TvRemoteCommandException
from metzctl import __doc__ as doc
from metzctl import __title__ as title


def main():
    epilog = "E.g. %(prog)s --ip 192.168.1.46 vup"
    parser = argparse.ArgumentParser(prog=title, description=doc, epilog=epilog)
    parser.add_argument("--ip", dest="ip", help="TV IP address", metavar="IP")
    parser.add_argument("--debug", dest="debug", action='store_true', help="Set verbose logging")
    parser.add_argument("-key", nargs=1, help="key code to be sent")
    parser.add_argument("-vup", action='store_true', help="volume up")
    parser.add_argument("-vdown", action='store_true', help="volume down")
    parser.add_argument("-chup", action='store_true', help="channel down")
    parser.add_argument("-chdown", action='store_true', help="channel down")
    parser.add_argument("-mute", action='store_true', help="mute")
    parser.add_argument("-ok", action='store_true', help="ok")
    parser.add_argument("-power", action='store_true', help="power")
    parser.add_argument("-on", action='store_true', help="Turns the TV on")
    parser.add_argument("--mac", dest="mac", metavar="MAC", help="Turns the TV on")
    parser.add_argument("-mac", action='store_true', help="Get the MAC for the passed IP")

    args = parser.parse_args()
    log_level = logging.INFO
    logging.basicConfig(format="%(message)s", level=log_level)

    config = {}
    config.update({k: v for k, v in vars(args).items() if v is not None})

    try:
        if args.on:
            if not args.mac:
                logging.warning("MAC address missing")
                return
            MetzRemote.power_on(args.mac)
        else:
            if not args.ip:
                logging.warning("IP address missing")
                return
            remote = MetzRemote(args.ip, debug=args.debug)
            if args.key:
                for key in args.key:
                    remote.control(key)
            elif args.vup:
                remote.volume_up()
            elif args.vdown:
                remote.volume_down()
            elif args.mute:
                remote.mute()
            elif args.chup:
                remote.ch_up()
            elif args.chdown:
                remote.ch_down()
            elif args.ok:
                remote.ok()
            elif args.power:
                remote.power()
            elif args.mac:
                logging.info("MAC {}".format(get_mac_address(ip=args.ip)))
            else:
                logging.warning("Warning: Unsupported option {}".format(args))

    except TvRemoteCommandException:
        logging.error("Error: Remote command failed")
    except Exception as e:
        logging.exception("Error: %s", str(e))


if __name__ == "__main__":
    main()
