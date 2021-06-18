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

ZONES_400 = [
    # Order
    MinimapZone(name="Shop", team="ORDER", x=35, y=370),
    MinimapZone(name="Base", team="ORDER", x=80, y=315),
    MinimapZone(name="T2 Top", team="ORDER", x=50, y=220),
    MinimapZone(name="T1 Top", team="ORDER", x=45, y=125),
    MinimapZone(name="Gromp", team="ORDER", x=75, y=175),
    MinimapZone(name="Blue Buff", team="ORDER", x=115, y=190),
    MinimapZone(name="Wolves", team="ORDER", x=115, y=225),
    MinimapZone(name="T2 Mid", team="ORDER", x=145, y=260),
    MinimapZone(name="T1 Mid", team="ORDER", x=185, y=215),
    MinimapZone(name="Raptors", team="ORDER", x=195, y=255),
    MinimapZone(name="Red Buff", team="ORDER", x=210, y=285),
    MinimapZone(name="Krugs", team="ORDER", x=225, y=320),
    MinimapZone(name="T2 Bot", team="ORDER", x=190, y=355),
    MinimapZone(name="T1 Bot", team="ORDER", x=280, y=355),
    # River
    MinimapZone(name="River Top", team="NEUTRAL", x=100, y=110),
    MinimapZone(name="Baron", team="NEUTRAL", x=140, y=130),
    MinimapZone(name="River Mid Top", team="NEUTRAL", x=170, y=170),
    MinimapZone(name="River Mid Bot", team="NEUTRAL", x=230, y=230),
    MinimapZone(name="Drake", team="NEUTRAL", x=265, y=275),
    MinimapZone(name="River Bot", team="NEUTRAL", x=300, y=290),
    # Chaos
    MinimapZone(name="Shop", team="ORDER", x=370, y=35),
    MinimapZone(name="Base", team="CHAOS", x=315, y=80),
    MinimapZone(name="T2 Top", team="CHAOS", x=220, y=50),
    MinimapZone(name="T1 Top", team="CHAOS", x=125, y=45),
    MinimapZone(name="Krugs", team="CHAOS", x=180, y=82),
    MinimapZone(name="Red Buff", team="CHAOS", x=195, y=115),
    MinimapZone(name="Raptors", team="CHAOS", x=212, y=148),
    MinimapZone(name="T2 Mid", team="CHAOS", x=260, y=145),
    MinimapZone(name="T1 Mid", team="CHAOS", x=215, y=185),
    MinimapZone(name="Wolves", team="CHAOS", x=293, y=179),
    MinimapZone(name="Blue Buff", team="CHAOS", x=295, y=215),
    MinimapZone(name="Gromp", team="CHAOS", x=330, y=225),
    MinimapZone(name="T2 Bot", team="CHAOS", x=355, y=190),
    MinimapZone(name="T1 Bot", team="CHAOS", x=355, y=280),
]
