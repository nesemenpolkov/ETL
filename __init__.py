from extract import Extractor

if __name__ == "__main__":
    test = Extractor(service="youtube", api_key="AIzaSyD49bsFeWc_Nvx-r5wuPy7RkPuiCFQN46E")
    test_sample = ["UC84J-P1AEat5jPz7C1vKhsw", "UC_IEcnNeHc_bwd92Ber-lew", "UCKonxxVHzDl55V7a9n_Nlgg",
                   "UCFU30dGHNhZ-hkh0R10LhLw", "UCsA_vkmuyIRlYYXeJueyIJQ", "UCdIEDjRlFiBdfQ0hqdSWHZw",
                   "UCQ4YOFsXjG9eXWZ6uLj2t2A", "Радіо Свобода Україна", "UCW5d-rpLATKOvBKs6heGuJw",
                   "SpastvRuchannel", "UC5azmFteRV-nj48bddT2z9w"]
    # x = test.get_channel_id("ХВАТИТМОЛЧАТЬРОССИЯ")
    # print(x)
    # test.video_stat(object_id="UC84J-P1AEat5jPz7C1vKhsw")
    test.monitor(channels=test_sample, interval=300, duration=48)
    test.run()
    #  test.get_activity("UC84J-P1AEat5jPz7C1vKhsw", True)
