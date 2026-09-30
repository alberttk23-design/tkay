#!/usr/bin/env python3
"""
Contents Intelligence Module
Provides aggregated Ad Copy, Creatives, Video Transcripts, Hooks, and Headlines
matching TrendTrack Advertising -> Contents view.
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "out", "spy_cache")

def get_contents_data(brand_name: str = "The Oodie") -> dict:
    # 1. Authentic datasets for The Oodie matching media_1790694514012.png - media_1790694544335.png
    ad_copies = [
        {
            "id": "cp_1",
            "thumbnail": "/static/emails/card_1.png",
            "text": "You LOVE us inside, now lets go out! 💙 Take classic Oodie comfort outdoors with cosiness that feels like you never left home:...",
            "ads_count": 45,
            "longest_running": "14 days"
        },
        {
            "id": "cp_2",
            "thumbnail": "/static/emails/card_2.png",
            "text": "We're putting the WIN in winter with 160 x 6 piece bundles to give away!",
            "ads_count": 45,
            "longest_running": "13 days"
        },
        {
            "id": "cp_3",
            "thumbnail": "/static/emails/card_4.png",
            "text": "Basics with main character energy...",
            "ads_count": 37,
            "longest_running": "2 days"
        },
        {
            "id": "cp_4",
            "thumbnail": "/static/emails/card_5.png",
            "text": "You know the Oodie™ Original — that oversized, wearable hug everyone's obsessed with. Now meet the version you can actually wear all day....",
            "ads_count": 33,
            "longest_running": "12 days"
        },
        {
            "id": "cp_5",
            "thumbnail": "/static/emails/card_6.png",
            "text": "🌸 Spring into savings... 🌸",
            "ads_count": 25,
            "longest_running": "1 day"
        },
        {
            "id": "cp_6",
            "thumbnail": "/static/emails/card_7.png",
            "text": "Hot sleeper? Keep your cool... 🩵",
            "ads_count": 23,
            "longest_running": "20 days"
        },
        {
            "id": "cp_7",
            "thumbnail": "/static/emails/card_8.png",
            "text": "Buy 1, get 1 free on Sleep Tee! It's that simple.",
            "ads_count": 23,
            "longest_running": "4 days"
        },
        {
            "id": "cp_8",
            "thumbnail": "/static/emails/card_9.png",
            "text": "Comfort has doubled with 2 FOR 1 on selected Oodie™ Originals! 💸",
            "ads_count": 20,
            "longest_running": "7 days"
        },
        {
            "id": "cp_9",
            "thumbnail": "/static/emails/card_10.png",
            "text": "The fabric is genuinely ridiculous. 😍",
            "ads_count": 19,
            "longest_running": "20 days"
        },
        {
            "id": "cp_10",
            "thumbnail": "/static/emails/card_11.png",
            "text": "Big enough to share, too good to actually do it... 🤭",
            "ads_count": 18,
            "longest_running": "14 days"
        }
    ]

    transcripts = [
        {
            "id": "tr_1",
            "thumbnail": "/static/emails/card_4.png",
            "text": "After my self-care night, my skin isn't the only thing that deserves luxury. The sleep tee from the OODIE is honestly the best part of the night. It's breathable, stretchy, and oversized. Basically what your body actually needs after self-care...",
            "ads_count": 3,
            "longest_running": "91 days",
            "has_linked_ads": False
        },
        {
            "id": "tr_2",
            "thumbnail": "/static/emails/card_8.png",
            "text": "Baby, baby, all right. Baby, baby, all right. Baby, baby, all right. Baby, baby, all right. Turn my phone on, vibrate, let it ring.",
            "ads_count": 3,
            "longest_running": "28 days",
            "has_linked_ads": False
        },
        {
            "id": "tr_3",
            "thumbnail": "/static/emails/card_10.png",
            "text": "I've started giving myself 10 minutes before the world gets access to me. Ever since I got my OODIE summer dressing gown, it has become the first thing I reach for after every shower...",
            "ads_count": 3,
            "longest_running": "25 days",
            "has_linked_ads": False
        },
        {
            "id": "tr_4",
            "thumbnail": "/static/emails/card_1.png",
            "text": "Can you buy one? Get one free! Udi Originals! Selected style! Oh wait! Shop now! Shop now! You can cut that off.",
            "ads_count": 3,
            "longest_running": "7 days",
            "has_linked_ads": False
        },
        {
            "id": "tr_5",
            "thumbnail": "/static/emails/card_6.png",
            "text": "Buy one, get one. Udi Originals. That's right, the Viral Udi Original. Experience unparalleled comfort. A wearable blanket designed for endless snuggles. Shop now before it's too late.",
            "ads_count": 3,
            "longest_running": "6 days",
            "has_linked_ads": False
        },
        {
            "id": "tr_6",
            "thumbnail": "/static/emails/card_7.png",
            "text": "This is why I stop wearing pajamas to bed. This is the Udi Sleep Tea. It's a super oversized tea made from the softest bamboo blend. It's incredibly stretchy, ultra light and super soft. The sleep tea also comes with two hidden pockets s...",
            "ads_count": 2,
            "longest_running": "90 days",
            "has_linked_ads": False
        },
        {
            "id": "tr_7",
            "thumbnail": "/static/emails/card_10.png",
            "text": "I started pretending the staycation is a boutique hotel. Love getting ready with the girls because there's zero rush so this is such a vibe. The summer robes are so soft, cozy and lightweight enough that you can move around freely doin...",
            "ads_count": 2,
            "longest_running": "25 days",
            "has_linked_ads": True
        },
        {
            "id": "tr_8",
            "thumbnail": "/static/emails/card_5.png",
            "text": "I need to talk about something that really annoys me if you're anything like me you have an entire wardrobe full of clothes jeans and every wash pajamas a complete afterthought and I think that's actually mad because a bad night's ...",
            "ads_count": 2,
            "longest_running": "20 days",
            "has_linked_ads": True
        },
        {
            "id": "tr_9",
            "thumbnail": "/static/emails/card_2.png",
            "text": "Stop scrolling if you love being comfortable. This is the Ooty Sleep Tea, and I refuse to believe this is just for sleepwear. I'd say this is my unofficial stay-at-home uniform because I wear it all day, every day. It's buttery soft, ultra-...",
            "ads_count": 2,
            "longest_running": "17 days",
            "has_linked_ads": False
        },
        {
            "id": "tr_10",
            "thumbnail": "/static/emails/card_11.png",
            "text": "getting into bed feels 10 times better when your PJs are actually comfortable. These are the Odie Cooling PJs and they're so perfect for every single night wear all year round. They're super lightweight and silky soft so you barely fee...",
            "ads_count": 2,
            "longest_running": "16 days",
            "has_linked_ads": False
        }
    ]

    hooks = [
        {
            "id": "hk_1",
            "thumbnail": "/static/emails/card_4.png",
            "text": "After my self-care night, my skin isn't the only thing that deserves luxury.",
            "ads_count": 3,
            "longest_running": "91 days"
        },
        {
            "id": "hk_2",
            "thumbnail": "/static/emails/card_8.png",
            "text": "Baby, baby, all right.",
            "ads_count": 3,
            "longest_running": "28 days"
        },
        {
            "id": "hk_3",
            "thumbnail": "/static/emails/card_10.png",
            "text": "I've started giving myself 10 minutes before the world gets access to me.",
            "ads_count": 3,
            "longest_running": "25 days"
        },
        {
            "id": "hk_4",
            "thumbnail": "/static/emails/card_1.png",
            "text": "Can you buy one?",
            "ads_count": 3,
            "longest_running": "7 days"
        },
        {
            "id": "hk_5",
            "thumbnail": "/static/emails/card_6.png",
            "text": "Buy one, get one. Udi Originals.",
            "ads_count": 3,
            "longest_running": "6 days"
        },
        {
            "id": "hk_6",
            "thumbnail": "/static/emails/card_7.png",
            "text": "This is why I stop wearing pajamas to bed. This is the Udi Sleep Tea.",
            "ads_count": 2,
            "longest_running": "90 days"
        },
        {
            "id": "hk_7",
            "thumbnail": "/static/emails/card_10.png",
            "text": "I started pretending the staycation is a boutique hotel.",
            "ads_count": 2,
            "longest_running": "25 days"
        },
        {
            "id": "hk_8",
            "thumbnail": "/static/emails/card_5.png",
            "text": "I need to talk about something that really annoys me if you're anything like me you have an entire",
            "ads_count": 2,
            "longest_running": "20 days"
        },
        {
            "id": "hk_9",
            "thumbnail": "/static/emails/card_2.png",
            "text": "Stop scrolling if you love being comfortable.",
            "ads_count": 2,
            "longest_running": "17 days"
        },
        {
            "id": "hk_10",
            "thumbnail": "/static/emails/card_11.png",
            "text": "getting into bed feels 10 times better when your PJs are actually comfortable. These are the Odie",
            "ads_count": 2,
            "longest_running": "16 days"
        },
        {
            "id": "hk_11",
            "thumbnail": "/static/emails/card_12.png",
            "text": "There's 30% off selected dirty blankets right now so obviously I have to investigate and by",
            "ads_count": 2,
            "longest_running": "11 days"
        }
    ]

    headlines = [
        {
            "id": "hl_1",
            "text": "🥰 Indoor energy. Outdoor attitude 🥰",
            "ads_count": 90,
            "longest_running": "14 days"
        },
        {
            "id": "hl_2",
            "text": "The Oodie™ Original Reimagined 🦄",
            "ads_count": 42,
            "longest_running": "11 days"
        },
        {
            "id": "hl_3",
            "text": "🔮 The Winter Wardrobe Reset 🔮",
            "ads_count": 38,
            "longest_running": "13 days"
        },
        {
            "id": "hl_4",
            "text": "Make Comfort Your Personality with Hoodies & Sweats 🥪",
            "ads_count": 35,
            "longest_running": "2 days"
        },
        {
            "id": "hl_5",
            "text": "💥 30% Off Selected Blankets 💥",
            "ads_count": 30,
            "longest_running": "11 days"
        },
        {
            "id": "hl_6",
            "text": "💖 NEW Cooling Pjs, Shamelessly Comfy 💖",
            "ads_count": 23,
            "longest_running": "20 days"
        },
        {
            "id": "hl_7",
            "text": "💸 Sleep Tees Sale! Double The Comfort, Half the Price 💸",
            "ads_count": 23,
            "longest_running": "4 days"
        },
        {
            "id": "hl_8",
            "text": "🚨 Flash Sale: Selected Licenses From £20! 🚨",
            "ads_count": 23,
            "longest_running": "1 day"
        },
        {
            "id": "hl_9",
            "text": "Meet The Oodie™ Original 👑",
            "ads_count": 21,
            "longest_running": "15 days"
        },
        {
            "id": "hl_10",
            "text": "🔥 Buy 1 Get 1 FREE on selected Oodie™ Originals 🔥",
            "ads_count": 20,
            "longest_running": "7 days"
        },
        {
            "id": "hl_11",
            "text": "Cooler days 💛 hotter deals! Up to $40 off... 🎒",
            "ads_count": 19,
            "longest_running": "3 days"
        },
        {
            "id": "hl_12",
            "text": "🚨 Our License Flash Sale Is Happening Now! 🚨",
            "ads_count": 19,
            "longest_running": "1 day"
        }
    ]

    creatives = [
        {
            "id": "cr_1",
            "type": "carousel",
            "title": "Multiple media",
            "pages": "1/4",
            "image": "/static/contents/creative_1.png",
            "badge": "Carousel",
            "ads_count": 24,
            "longest_running": "14 days"
        },
        {
            "id": "cr_2",
            "type": "image",
            "title": "£70K PRIZE DRAW GIVEAWAY",
            "subtitle": "160 Bundles, 160 Winners",
            "image": "/static/contents/creative_2.png",
            "badge": "Image",
            "ads_count": 45,
            "longest_running": "13 days"
        },
        {
            "id": "cr_3",
            "type": "meme",
            "title": "me when theres 30% Off Selected Blankets*",
            "subtitle": "i...lowkey need a blanket",
            "image": "/static/contents/creative_3.png",
            "badge": "Meme",
            "ads_count": 30,
            "longest_running": "11 days"
        },
        {
            "id": "cr_4",
            "type": "meme",
            "title": "me when theres 30% Off Selected Blankets*",
            "subtitle": "i...lowkey need a blanket",
            "image": "/static/contents/creative_4.png",
            "badge": "Meme",
            "ads_count": 28,
            "longest_running": "11 days"
        },
        {
            "id": "cr_5",
            "type": "video",
            "title": "Self-care Night routine",
            "subtitle": "Viral Sleep Tee",
            "image": "/static/emails/card_4.png",
            "badge": "Video",
            "ads_count": 18,
            "longest_running": "91 days"
        },
        {
            "id": "cr_6",
            "type": "image",
            "title": "Cooling Blankets",
            "subtitle": "Keep the blanket, lose the heat",
            "image": "/static/emails/card_7.png",
            "badge": "Image",
            "ads_count": 23,
            "longest_running": "20 days"
        },
        {
            "id": "cr_7",
            "type": "carousel",
            "title": "Summer Robes",
            "pages": "1/3",
            "image": "/static/emails/card_10.png",
            "badge": "Carousel",
            "ads_count": 19,
            "longest_running": "25 days"
        },
        {
            "id": "cr_8",
            "type": "dynamic",
            "title": "Buy 1 Get 1 Free Sleep Tee",
            "subtitle": "Selected styles while stocks last",
            "image": "/static/emails/card_8.png",
            "badge": "Dynamic",
            "ads_count": 23,
            "longest_running": "4 days"
        }
    ]

    return {
        "brand": brand_name,
        "counts": {
            "ad_copies": 141,
            "transcripts": 29,
            "hooks": 29,
            "headlines": 128,
            "creatives": 64
        },
        "ad_copies": ad_copies,
        "transcripts": transcripts,
        "hooks": hooks,
        "headlines": headlines,
        "creatives": creatives
    }

if __name__ == "__main__":
    data = get_contents_data("The Oodie")
    print("Contents data keys:", list(data.keys()))
