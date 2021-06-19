from .models import MinimapZone


ZONES = [
    # Order
    MinimapZone(name="Shop", team="ORDER", x=35, y=390),
    MinimapZone(name="Nexus", team="ORDER", x=60, y=360),
    # Order Top
    MinimapZone(name="Top T3", team="ORDER", x=50, y=300),
    MinimapZone(name="Top T2", team="ORDER", x=60, y=235),
    MinimapZone(name="Top T1", team="ORDER", x=45, y=135),
    # Order Mid
    MinimapZone(name="Mid T3", team="ORDER", x=115, y=310),
    MinimapZone(name="Mid T2", team="ORDER", x=150, y=280),
    MinimapZone(name="Mid T1", team="ORDER", x=170, y=240),
    # Order Bot
    MinimapZone(name="Bot T3", team="ORDER", x=130, y=370),
    MinimapZone(name="Bot T2", team="ORDER", x=200, y=365),
    MinimapZone(name="Bot T1", team="ORDER", x=285, y=375),
    # Order Jungle Top
    MinimapZone(name="Gromp", team="ORDER", x=75, y=185),
    MinimapZone(name="Blue Buff", team="ORDER", x=115, y=200),
    MinimapZone(name="Wolves", team="ORDER", x=115, y=235),
    # Order Jungle Bot
    MinimapZone(name="Raptors", team="ORDER", x=205, y=265),
    MinimapZone(name="Red Buff", team="ORDER", x=220, y=300),
    MinimapZone(name="Krugs", team="ORDER", x=240, y=335),
    # Neutral Top
    MinimapZone(name="Toplane", team="NEUTRAL", x=70, y=70),
    MinimapZone(name="Top River", team="NEUTRAL", x=100, y=115),
    MinimapZone(name="Baron", team="NEUTRAL", x=148, y=132),
    MinimapZone(name="Top Scuttle", team="NEUTRAL", x=135, y=155),
    # Neutral Mid
    MinimapZone(name="Mid Top River", team="NEUTRAL", x=177, y=177),
    MinimapZone(name="Midlane", team="NEUTRAL", x=210, y=210),
    MinimapZone(name="Mid Bot River", team="NEUTRAL", x=240, y=240),
    # Neutral Bot
    MinimapZone(name="Drake", team="NEUTRAL", x=280, y=290),
    MinimapZone(name="Bot Scuttle", team="NEUTRAL", x=292, y=270),
    MinimapZone(name="Bot River", team="NEUTRAL", x=320, y=310),
    MinimapZone(name="Botlane", team="NEUTRAL", x=350, y=345),
    # Chaos
    MinimapZone(name="Shop", team="CHAOS", x=390, y=35),
    MinimapZone(name="Nexus", team="CHAOS", x=360, y=60),
    # Chaos Top
    MinimapZone(name="Top T3", team="CHAOS", x=300, y=50),
    MinimapZone(name="Top T2", team="CHAOS", x=235, y=60),
    MinimapZone(name="Top T1", team="CHAOS", x=135, y=45),
    # Chaos Mid
    MinimapZone(name="Mid T3", team="CHAOS", x=310, y=115),
    MinimapZone(name="Mid T2", team="CHAOS", x=280, y=150),
    MinimapZone(name="Mid T1", team="CHAOS", x=240, y=170),
    # Chaos Bot
    MinimapZone(name="Bot T3", team="CHAOS", x=370, y=130),
    MinimapZone(name="Bot T2", team="CHAOS", x=365, y=200),
    MinimapZone(name="Bot T1", team="CHAOS", x=375, y=285),
    # Chaos Jungle Top
    MinimapZone(name="Krugs", team="CHAOS", x=188, y=85),
    MinimapZone(name="Red Buff", team="CHAOS", x=203, y=120),
    MinimapZone(name="Raptors", team="CHAOS", x=222, y=154),
    # Chaos Jungle Top
    MinimapZone(name="Wolves", team="CHAOS", x=308, y=186),
    MinimapZone(name="Blue Buff", team="CHAOS", x=308, y=224),
    MinimapZone(name="Gromp", team="CHAOS", x=348, y=236),
]
