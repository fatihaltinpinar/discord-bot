import os
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
OPENDOTA_KEY = os.getenv("OPENDOTA_KEY")


ABOUT = """
Ben <@118406756589109255>'nin kolesiyim, sunucunuzda otururum, bos yaparim
- Dota ses seysileri
- Hangi muzzukler caliniyor listesi vs."""

WIN_MESSAGE = ["Türk Dotası Kazandı", "Midden YARdık", "Win", "+20 +20 +20", "Zafer"]
LOSS_MESSAGE = ["Türk Dotası Hüsran", "Kaybeden Tayfa", "Olmadı :(", "-20, -20 -20", "Mağlubiyet"]

TITLE_PADDING = 50

WIN_DESCRIPTIONS = ["Ne oynadım be",
                    "Midi ezdim",
                    "Kuşu banlamadılar",
                    "Dövüşen hero aldık",
                    "Benim kumarım biter",
                    "Ellerinize sağlık",
                    "Taşıdım, taşıdım, biz ezmeseydik nerdee...",
                    "Space açtık o kadar",
                    "Karşıdaki adam maldı yoksa kaybetmiştik",
                    "Bide divine adam XDDXDXDXDXDXD"]
LOSS_DESCRIPTIONS = ["Ben arkada 5 kişi kesiyodum siz kime öldünüz",
                     "Kuşu banladılar",
                     "Midi ezmiştim",
                     "X alan kaybetmeye mahkumdur",
                     "Biz lane'i kazanmıştık abi bilmiom valla",
                     "İki tane pos 5",
                     "Abi bana sölemionuz ki ne yapcamı",
                     "Şu ağacı kırmadın pull yapamadım",
                     "Benim kumarım biter"]

OWNER_ID = 118406756589109255
DOTA_APP_ID = 356875988589740042
OWNER_STEAM_ID = "92290827"

DOTA_STATUS_CHANNEL_ID = 211239805307191298

INVITE_LINK = "https://discord.com/api/oauth2/authorize?client_id=722778335540936724&permissions=3271680&scope=bot"

MUSIC_BOT_ID = 234395307759108106
PREFIX = "."
