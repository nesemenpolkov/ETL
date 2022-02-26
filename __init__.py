from extract import Extractor
import os
import logging
from config import logfile

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename=logfile)
    log = logging.getLogger(__name__)
    try:
        test = Extractor(service="youtube", api_key="AIzaSyBNzgGm3NTIPH4P1hyZXW7qsB84_xDQKI0")
        test_sample = ["UC84J-P1AEat5jPz7C1vKhsw", "UC_IEcnNeHc_bwd92Ber-lew", "UCKonxxVHzDl55V7a9n_Nlgg",
                       "UCFU30dGHNhZ-hkh0R10LhLw", "UCsA_vkmuyIRlYYXeJueyIJQ", "UCdIEDjRlFiBdfQ0hqdSWHZw",
                       "UCQ4YOFsXjG9eXWZ6uLj2t2A", "UC7qnYpVcuFbURi3E2E6_f6Q", "UCW5d-rpLATKOvBKs6heGuJw",
                       "SpastvRuchannel", "UC5azmFteRV-nj48bddT2z9w", "UCAyoyj6QDZR4HU_kOLrPSsg",
                       "UCBi2mrWuNuyYy4gbM6fU18Q", "UC101o-vQ2iOj9vr00JUlyKw", "UCz63ar5uANqYTKJIwnUQucw",
                       "UCsAw3WynQJMm7tMy093y37A"]
        # x = test.get_channel_id("ХВАТИТМОЛЧАТЬРОССИЯ")
        # print(x)
        # test.video_stat(object_id="UC84J-P1AEat5jPz7C1vKhsw")
        test.monitor(channels=test_sample, interval=300, duration=48, delta=900)
        test.run(isBackground=True)
        #  test.get_activity("UC84J-P1AEat5jPz7C1vKhsw", True)
    except Exception as e:
        log.exception(e)
        print("[ERROR]:", e)
        if not os.path.exists("exceptions.txt"):
            with open("exceptions.txt", "w") as f:
                f.write(e)
        else:
            with open("exceptions.txt", "a") as f:
                f.write(e)

        # reserve key AIzaSyBNzgGm3NTIPH4P1hyZXW7qsB84_xDQKI0
        # main key AIzaSyD49bsFeWc_Nvx-r5wuPy7RkPuiCFQN46E
