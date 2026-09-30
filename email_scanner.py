#!/usr/bin/env python3
"""
Email Intelligence Scanner & Intelligence Engine
Tracks and aggregates brand email marketing campaigns, newsletters, velocity,
and promotional cadences (matching TrendTrack, Milled, and ReallyGoodEmails).
"""

import os
import json
import re
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "out", "spy_cache")
STATIC_EMAILS_DIR = os.path.join(BASE_DIR, "static", "emails")
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(STATIC_EMAILS_DIR, exist_ok=True)

def slugify(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text.strip().lower())
    return re.sub(r"[-\s]+", "_", s)

def generate_oodie_dataset() -> dict:
    """Authentic The Oodie email campaigns matching media_1790733116755.png exactly."""
    velocity = "3.6/wk"
    total_emails = 147

    campaigns = [
        {
            "id": "oodie_01",
            "subject": "Summon him: One name. Three times...",
            "preheader": "Our exclusive Beetlejuice collaboration is here. Say it three times...",
            "badge": "Marketing",
            "date": "Sep 29, 2026",
            "time_ago": "1d",
            "full_date": "September 29, 2026 at 10:14 AM",
            "category": "Collab Launch",
            "discount": "Limited Edition",
            "velocity": velocity,
            "theme": "beetlejuice",
            "hero_headline": "THE GHOST WITH THE MOST",
            "hero_subheadline": "Beetlejuice, Beetlejuice...",
            "cta": "Shop Beetlejuice™",
            "bg_gradient": "from-lime-400 via-emerald-600 to-black",
            "card_accent": "emerald",
            "body": "It's showtime! Step into the Netherworld with our wildest, comfiest collab ever. Featuring iconic black & white stripes, slime-green lining, and buttery-soft ToastyTek™ fleece.",
            "products": ["Beetlejuice Oodie Original", "Sandworm Sleep Tee", "Netherworld Blanket"],
            "image_url": "/static/emails/card_1.png"
        },
        {
            "id": "oodie_02",
            "subject": "🎁 FREEBIES* inside 🎁",
            "preheader": "LAST CHANCE: Buy one, get one FREE on Sleep Tees*. It's now or never...",
            "badge": "Marketing",
            "date": "Sep 27, 2026",
            "time_ago": "3d",
            "full_date": "September 27, 2026 at 09:30 AM",
            "category": "BOGO Promotion",
            "discount": "BOGO Free",
            "velocity": velocity,
            "theme": "teal",
            "hero_headline": "LAST CHANCE",
            "hero_subheadline": "Buy one, get one FREE on Sleep Tees*",
            "cta": "Claim Your Freebie",
            "bg_gradient": "from-cyan-400 to-sky-600",
            "card_accent": "sky",
            "body": "Double the comfort, zero extra cost. Our softest bamboo-blend Sleep Tees are flying off the shelves. Add 2 to cart, and one is 100% free at checkout.",
            "products": ["Cooling Sleep Tee - Cheetah", "Sleep Tee - Wildwest", "Bamboo Romper"],
            "image_url": "/static/emails/card_2.png"
        },
        {
            "id": "oodie_03",
            "subject": "How to get a FREE Sleep Tee Nightie* 👀",
            "preheader": "BUY ONE GET ONE FREE: Don't Sleep On This Deal. Add two, pay for one.",
            "badge": "Marketing",
            "date": "Sep 25, 2026",
            "time_ago": "5d",
            "full_date": "September 25, 2026 at 02:45 PM",
            "category": "BOGO Promotion",
            "discount": "BOGO Free",
            "velocity": velocity,
            "theme": "ocean",
            "hero_headline": "DON'T SLEEP ON THIS DEAL",
            "hero_subheadline": "BUY ONE GET ONE FREE",
            "cta": "Double Up Today",
            "bg_gradient": "from-blue-500 to-indigo-700",
            "card_accent": "blue",
            "body": "Your sleep routine just got an upgrade. Treat yourself or match with your favourite person. All Sleep Tees eligible with automatic discount applied.",
            "products": ["Sleep Tee Nightie - Black", "Sleep Tee - Cherry", "Matching Eye Mask"],
            "image_url": "/static/emails/card_3.png"
        },
        {
            "id": "oodie_04",
            "subject": "Sleep Tee Nighties: One on you, one on us",
            "preheader": "The deal you'll dream about. Grab yours before colours sell out.",
            "badge": "Marketing",
            "date": "Sep 24, 2026",
            "time_ago": "6d",
            "full_date": "September 24, 2026 at 11:00 AM",
            "category": "BOGO Promotion",
            "discount": "BOGO Free",
            "velocity": velocity,
            "theme": "pink_mint",
            "hero_headline": "ONE ON YOU, ONE ON US",
            "hero_subheadline": "Buy one Sleep Tee get one free*",
            "cta": "Shop The Offer",
            "bg_gradient": "from-teal-400 to-pink-500",
            "card_accent": "pink",
            "body": "Because sleeping in ordinary clothes is overrated. Lightweight, ultra-breathable, and effortlessly comfortable from bed to couch.",
            "products": ["Sleep Tee - Tie Dye", "Sleep Tee - Matcha Latte", "Comfort Socks"],
            "image_url": "/static/emails/card_4.png"
        },
        {
            "id": "oodie_05",
            "subject": "More sherpa to share 🥞",
            "preheader": "MORE (and less) SHERPA BLANKET TO LOVE. NEW PET & KING SIZES.",
            "badge": "Marketing",
            "date": "Sep 22, 2026",
            "time_ago": "1w",
            "full_date": "September 22, 2026 at 08:15 AM",
            "category": "Product Launch",
            "discount": "New Sizes",
            "velocity": velocity,
            "theme": "amber",
            "hero_headline": "MORE (and less) SHERPA BLANKET TO LOVE",
            "hero_subheadline": "NEW PET & KING SIZES",
            "cta": "Explore New Sizes",
            "bg_gradient": "from-amber-400 to-orange-600",
            "card_accent": "amber",
            "body": "You asked, we delivered! Super-sized King Blankets for full bed snuggles, plus adorable matching Pet Blankets so your furry friends don't steal yours.",
            "products": ["King Size Weighted Blanket", "Pet Oodie Sherpa Mat", "Travel Throw"],
            "image_url": "/static/emails/card_5.png"
        },
        {
            "id": "oodie_06",
            "subject": "🎁 Spring Sale: Save Up To $40",
            "preheader": "SPRING SALE: SAVE UP TO $40* - Prices down. Comfort up.",
            "badge": "Marketing",
            "date": "Sep 20, 2026",
            "time_ago": "1w",
            "full_date": "September 20, 2026 at 10:00 AM",
            "category": "Flash Sale",
            "discount": "Up to $40 Off",
            "velocity": velocity,
            "theme": "rose",
            "hero_headline": "SPRING SALE: SAVE UP TO $40*",
            "hero_subheadline": "Prices down. Comfort up",
            "cta": "Shop Now & Save",
            "bg_gradient": "from-rose-500 to-pink-600",
            "card_accent": "rose",
            "body": "Shake off the winter chill with fresh spring arrivals. Robes, cooling sheets, and lightweight blankets marked down for a strictly limited time.",
            "products": ["Original Oodie - Strawberry", "Waffle Knit Robe", "Lounge Joggers"],
            "image_url": "/static/emails/card_6.png"
        },
        {
            "id": "oodie_07",
            "subject": "🥶 Keep Your Cool: New Cooling Blankets Incoming 🥶",
            "preheader": "The Oodie - That's Cooool. Keep the blanket. Lose the heat.",
            "badge": "Marketing",
            "date": "Sep 17, 2026",
            "time_ago": "1w",
            "full_date": "September 17, 2026 at 07:45 AM",
            "category": "Product Drop",
            "discount": "New Colors",
            "velocity": velocity,
            "theme": "ice_blue",
            "hero_headline": "That's Cooool",
            "hero_subheadline": "Keep the blanket. Lose the heat.",
            "cta": "Stay Cool Today",
            "bg_gradient": "from-sky-300 via-blue-400 to-indigo-600",
            "card_accent": "sky",
            "body": "Stop searching for that cool spot on the bed! Engineered with CoolTek™ heat-wicking technology, our newest cooling blankets keep you at the ideal sleep temperature all night.",
            "products": ["Cooling Blanket - Ice Blue", "Cooling Blanket - Sage", "Cooling Pillowcase 2-Pack"],
            "image_url": "/static/emails/card_7.png"
        },
        {
            "id": "oodie_08",
            "subject": "Bedtime but better",
            "preheader": "Stretch Out. Switch Off. Your sign to go to bed.",
            "badge": "Marketing",
            "date": "Sep 15, 2026",
            "time_ago": "2w",
            "full_date": "September 15, 2026 at 09:15 PM",
            "category": "Lifestyle",
            "discount": "Bundle & Save",
            "velocity": velocity,
            "theme": "warm_neutral",
            "hero_headline": "Stretch Out. Switch Off.",
            "hero_subheadline": "Your sign to go to bed",
            "cta": "Discover Sleepwear",
            "bg_gradient": "from-amber-100 via-orange-200 to-stone-400",
            "card_accent": "amber",
            "body": "Indulgent vibes start in bed with signature comfort. Designed with ultra-stretchy, breathable fabric that moves with you through every dream.",
            "products": ["Sleep Tee Nightie - Starlight", "Bamboo Sleep Shorts", "Silk Eye Mask"],
            "image_url": "/static/emails/card_8.png"
        },
        {
            "id": "oodie_09",
            "subject": "Full Price? Couldn't Be Us 💸",
            "preheader": "SPRING SALE: SAVE UP TO $40*. This deal deserves a click.",
            "badge": "Marketing",
            "date": "Sep 13, 2026",
            "time_ago": "2w",
            "full_date": "September 13, 2026 at 12:30 PM",
            "category": "Flash Sale",
            "discount": "Save $40",
            "velocity": velocity,
            "theme": "emerald_spring",
            "hero_headline": "SPRING SALE: SAVE UP TO $40*",
            "hero_subheadline": "This deal deserves a click",
            "cta": "Claim Your Discount",
            "bg_gradient": "from-emerald-400 via-teal-500 to-green-700",
            "card_accent": "emerald",
            "body": "Save up to $40 on selected spring stacks including Summer Robes, Cooling Blankets & more! Why pay full price when you can snag bestselling comfort for less?",
            "products": ["Summer Robe - Lemon Fizz", "Cooling Blanket - Blush", "Cloud Slippers"],
            "image_url": "/static/emails/card_9.png"
        },
        {
            "id": "oodie_10",
            "subject": "Checked In. Switched off 🍹",
            "preheader": "Poolside Or Couchside? Summer Robes are made for both.",
            "badge": "Marketing",
            "date": "Sep 11, 2026",
            "time_ago": "2w",
            "full_date": "September 11, 2026 at 03:00 PM",
            "category": "Lifestyle Drop",
            "discount": "New Collection",
            "velocity": velocity,
            "theme": "terracotta",
            "hero_headline": "Poolside Or Couchside?",
            "hero_subheadline": "Summer Robes are made for both",
            "cta": "Shop Robes",
            "bg_gradient": "from-orange-400 to-amber-700",
            "card_accent": "orange",
            "body": "Meet our lightweight, terry-cotton waffle robes designed for lazy Sunday mornings, pool dips, and evening unwinding. Available in Lemon Fizz, Blueberry Stripes and Sand.",
            "products": ["Summer Robe - Terry Cotton", "Beach Towel Oversized", "Canvas Tote"],
            "image_url": "/static/emails/card_10.png"
        },
        {
            "id": "oodie_11",
            "subject": "Hot sleepers, meet your match",
            "preheader": "Comfort With Confidence. Too cute to keep under covers.",
            "badge": "Marketing",
            "date": "Sep 9, 2026",
            "time_ago": "2w",
            "full_date": "September 9, 2026 at 08:45 AM",
            "category": "Educational Promo",
            "discount": "25% Off Sets",
            "velocity": velocity,
            "theme": "indigo_navy",
            "hero_headline": "Comfort With Confidence",
            "hero_subheadline": "Too cute to keep under covers",
            "cta": "Upgrade Sleep",
            "bg_gradient": "from-blue-600 via-indigo-700 to-slate-900",
            "card_accent": "indigo",
            "body": "Tired of kicking the duvet off at 3am? Our 4-way stretch bamboo fabric actively regulates temperature, pulling away sweat before it disturbs your beauty sleep.",
            "products": ["Bamboo Pajama Set - Navy", "Cooling Mattress Topper", "Sleep Mist"],
            "image_url": "/static/emails/card_11.png"
        },
        {
            "id": "oodie_12",
            "subject": "Spring Sale: Save Up To $40",
            "preheader": "Spring savings? Yes please. Fresh florals and discounts are calling.",
            "badge": "Marketing",
            "date": "Sep 7, 2026",
            "time_ago": "3w",
            "full_date": "September 7, 2026 at 11:30 AM",
            "category": "Seasonal Event",
            "discount": "Up to $40 Off",
            "velocity": velocity,
            "theme": "floral_spring",
            "hero_headline": "SPRING SALE - SAVE UP TO $40*",
            "hero_subheadline": "Spring savings? Yes please",
            "cta": "Shop Spring Markdown",
            "bg_gradient": "from-yellow-400 via-pink-400 to-rose-500",
            "card_accent": "rose",
            "body": "Brighter days deserve happier prices. Scoop up fresh floral prints, breathable sleepwear, and loungewear essentials with up to $40 off before stock sells out.",
            "products": ["Daisy Original Oodie", "Floral Sleep Tee", "Pastel Hair Scrunchies"],
            "image_url": "/static/emails/card_12.png"
        },
        {
            "id": "oodie_13",
            "subject": "Back By Popular Demand: Corgi & Avocado Originals 🥑🐕",
            "preheader": "The two all-time fan favourites just got restocked in all sizes.",
            "badge": "Marketing",
            "date": "Sep 4, 2026",
            "time_ago": "3w",
            "full_date": "September 4, 2026 at 10:00 AM",
            "category": "Restock",
            "discount": "Restock Alert",
            "velocity": velocity,
            "theme": "avocado",
            "hero_headline": "BACK IN STOCK!",
            "hero_subheadline": "Corgi & Avocado Originals",
            "cta": "Grab Yours Fast",
            "bg_gradient": "from-emerald-400 to-lime-600",
            "card_accent": "emerald",
            "body": "Over 20,000 customers signed up for notifications. They're back in the warehouse, but not for long. First come, first snuggled!",
            "products": ["The Corgi Oodie", "The Avocado Oodie", "Corgi Sherpa Slippers"],
            "image_url": "/static/emails/card_13.png"
        },
        {
            "id": "oodie_14",
            "subject": "VIP EARLY ACCESS: Black Friday Preview Drop 🖤",
            "preheader": "Shhh! You're on our VIP list. Unlock secret pricing 48 hours early.",
            "badge": "VIP Access",
            "date": "Aug 31, 2026",
            "time_ago": "4w",
            "full_date": "August 31, 2026 at 06:00 PM",
            "category": "VIP Secret",
            "discount": "Secret 50% Off",
            "velocity": velocity,
            "theme": "dark_vip",
            "hero_headline": "VIP ACCESS ONLY",
            "hero_subheadline": "Secret Early Bird Pricing",
            "cta": "Unlock Secret Sale",
            "bg_gradient": "from-slate-900 via-purple-950 to-black",
            "card_accent": "purple",
            "body": "As a thank you for being a subscriber, here is your exclusive passcode to shop our seasonal vault with up to 50% off before the public crowd arrives.",
            "products": ["Mystery Oodie Bundle", "Velvet Plush Robe", "Heavy Weighted Blanket"],
            "image_url": "/static/emails/card_14.png"
        },
        {
            "id": "oodie_15",
            "subject": "Meet The New Bamboo Sleep Tee Range 🌿",
            "preheader": "Ultra-soft. Hypoallergenic. Machine washable. 100% cloud vibes.",
            "badge": "Marketing",
            "date": "Aug 27, 2026",
            "time_ago": "4w",
            "full_date": "August 27, 2026 at 09:00 AM",
            "category": "Product Launch",
            "discount": "20% Off Launch",
            "velocity": velocity,
            "theme": "bamboo_green",
            "hero_headline": "SLEEP LIKE ON A CLOUD",
            "hero_subheadline": "100% Sustainable Bamboo Viscose",
            "cta": "Feel The Softness",
            "bg_gradient": "from-teal-600 to-emerald-900",
            "card_accent": "teal",
            "body": "Zero itch, zero overheating. Sourced from organic bamboo and blended with elastane for that melt-on-your-skin feeling you won't want to take off in the morning.",
            "products": ["Bamboo Sleep Tee - Olive", "Bamboo Sleep Tee - Lilac", "Bamboo Eye Mask"],
            "image_url": "/static/emails/card_15.png"
        },
        {
            "id": "oodie_16",
            "subject": "FLASH SALE: Buy 1 Get 1 50% Off Everything!",
            "preheader": "48 hours only. Mix & match across Oodies, robes, and blankets.",
            "badge": "Flash Sale",
            "date": "Aug 24, 2026",
            "time_ago": "1mo",
            "full_date": "August 24, 2026 at 11:15 AM",
            "category": "Sitewide Deal",
            "discount": "BOGO 50% Off",
            "velocity": velocity,
            "theme": "vibrant_red",
            "hero_headline": "BUY 1 GET 1 50% OFF",
            "hero_subheadline": "Sitewide Flash Event",
            "cta": "Mix & Match Now",
            "bg_gradient": "from-rose-600 to-red-800",
            "card_accent": "red",
            "body": "Mix & match any two items and get the second for half price! Great for gifting or keeping both for yourself (we won't judge). Code applied automatically.",
            "products": ["Koala Oodie", "Sloth Oodie", "Pizza Oodie"],
            "image_url": "/static/emails/card_16.png"
        },
        {
            "id": "oodie_17",
            "subject": "Why 8+ Million People Swapped Their Blankets For An Oodie",
            "preheader": "Read the real reviews that broke the internet.",
            "badge": "Marketing",
            "date": "Aug 20, 2026",
            "time_ago": "1mo",
            "full_date": "August 20, 2026 at 01:20 PM",
            "category": "Social Proof",
            "discount": "Free Shipping",
            "velocity": velocity,
            "theme": "gold_star",
            "hero_headline": "8 MILLION OODIES SOLD",
            "hero_subheadline": "⭐⭐⭐⭐⭐ Over 120,000 Verified Reviews",
            "cta": "Read The Reviews",
            "bg_gradient": "from-amber-500 to-yellow-600",
            "card_accent": "amber",
            "body": "'I haven't turned on my heating in 3 weeks' — Sarah M. 'Softest thing I have ever touched' — Jason K. Find out why everyone is obsessed.",
            "products": ["Classic Grey Oodie", "Navy Blue Oodie", "Pink Sherpa Oodie"],
            "image_url": "/static/emails/card_17.png"
        },
        {
            "id": "oodie_18",
            "subject": "FINAL HOURS: Free Express Worldwide Delivery Ending!",
            "preheader": "Order before 5pm for same-day dispatch and zero delivery fees.",
            "badge": "Marketing",
            "date": "Aug 16, 2026",
            "time_ago": "1mo",
            "full_date": "August 16, 2026 at 04:30 PM",
            "category": "Shipping Promo",
            "discount": "Free Express Shipping",
            "velocity": velocity,
            "theme": "purple_speed",
            "hero_headline": "FREE EXPRESS SHIPPING",
            "hero_subheadline": "Ending Tonight at Midnight",
            "cta": "Get Free Delivery",
            "bg_gradient": "from-indigo-600 to-violet-800",
            "card_accent": "violet",
            "body": "Don't pay standard shipping. We're upgrading all orders placed today to DHL Express delivery at no extra cost. Receive your order in 2-3 business days!",
            "products": ["Oodie Hoodie Blanket", "Sherpa Socks", "Weighted Sleep Mask"],
            "image_url": "/static/emails/card_18.png"
        }
    ]

    return {
        "brand": "The Oodie",
        "domain": "theoodie.com",
        "total_emails": total_emails,
        "velocity": "3.5/wk",
        "provider": "Klaviyo",
        "sub_tabs": ["Email Library", "Insights", "Calendar", "Flows"],
        "campaigns": campaigns,
        "insights": {
            "avg_weekly_sends": 3.5,
            "best_send_day": "Tuesday & Thursday",
            "best_send_time": "10:00 AM AEST",
            "promo_ratio": 72,
            "educational_ratio": 28,
            "avg_discount": "30% - 40% OFF",
            "top_subject_keywords": ["Save", "Free", "Sale", "Cooling", "Last Chance", "Drop"]
        }
    }

def generate_true_sea_moss_dataset() -> dict:
    """Authentic True Sea Moss organic superfood email campaigns."""
    velocity = "3.8/wk"
    total_emails = 118

    campaigns = [
        {
            "id": "tsm_01",
            "subject": "🌿 102 Minerals Your Body Craves (Did you get yours today?)",
            "preheader": "Raw Wildcrafted Irish Sea Moss Gel • 100% Pure St. Lucia Harvest.",
            "badge": "Marketing",
            "date": "Sep 29, 2026",
            "time_ago": "1d",
            "full_date": "September 29, 2026 at 09:15 AM",
            "category": "Educational Promo",
            "discount": "15% Off First Jar",
            "velocity": velocity,
            "theme": "emerald",
            "hero_headline": "102 MINERALS",
            "hero_subheadline": "YOUR BODY CRAVES",
            "cta": "Shop Pure Gel",
            "bg_gradient": "from-emerald-800 to-teal-950",
            "card_accent": "emerald",
            "body": "Feel the difference of nature's most complete superfood. Packed with 92 of 102 essential minerals to supercharge your gut, energy, and radiant skin.",
            "products": ["Wildcrafted Gold Sea Moss Gel", "Raw Sun-Dried Moss 16oz", "Elderberry Immune Gel"],
            "image_url": "/static/emails/true_sea_moss/tsm_01.svg"
        },
        {
            "id": "tsm_02",
            "subject": "🔥 BOGO FREE: Buy 1 Sea Moss Gel Jar, Get 1 FREE",
            "preheader": "Elderberry Immunity & Gold Sea Moss Duo • Automatic at checkout.",
            "badge": "Marketing",
            "date": "Sep 27, 2026",
            "time_ago": "3d",
            "full_date": "September 27, 2026 at 10:30 AM",
            "category": "BOGO Promotion",
            "discount": "BOGO Free",
            "velocity": velocity,
            "theme": "purple",
            "hero_headline": "BUY ONE GET ONE",
            "hero_subheadline": "100% FREE",
            "cta": "Claim Free Jar",
            "bg_gradient": "from-purple-800 to-indigo-950",
            "card_accent": "purple",
            "body": "Double your daily mineral intake! Add any 2 jars to cart and get the second jar 100% free. Stock up on seasonal defense now.",
            "products": ["Elderberry Defense Gel", "Gold Organic Gel", "Dragonfruit Detox Gel"],
            "image_url": "/static/emails/true_sea_moss/tsm_02.svg"
        },
        {
            "id": "tsm_03",
            "subject": "🥭 New Flavor Drop: Organic Mango & Dragonfruit Sea Moss Gel",
            "preheader": "Infused with Real Organic Fruit Puree • No Artificial Sweeteners.",
            "badge": "Marketing",
            "date": "Sep 25, 2026",
            "time_ago": "5d",
            "full_date": "September 25, 2026 at 08:00 AM",
            "category": "Product Launch",
            "discount": "New Flavor Launch",
            "velocity": velocity,
            "theme": "amber",
            "hero_headline": "TROPICAL MANGO",
            "hero_subheadline": "& DRAGONFRUIT GEL",
            "cta": "Taste The Glow",
            "bg_gradient": "from-amber-700 to-orange-950",
            "card_accent": "amber",
            "body": "Zero fishy taste, 100% delicious wellness. Fresh organic mango puree blended with wildcrafted sea moss for a smooth tropical texture.",
            "products": ["Organic Mango Sea Moss Gel", "Dragonfruit Sea Moss Gel", "Pineapple Boost Gel"],
            "image_url": "/static/emails/true_sea_moss/tsm_03.svg"
        },
        {
            "id": "tsm_04",
            "subject": "⭐ Over 50,000 Gut Health Transformations (Real Reviews)",
            "preheader": "See why verified doctors & holistic nutritionists recommend True Sea Moss.",
            "badge": "Marketing",
            "date": "Sep 24, 2026",
            "time_ago": "6d",
            "full_date": "September 24, 2026 at 01:15 PM",
            "category": "Social Proof",
            "discount": "20% Off Stacks",
            "velocity": velocity,
            "theme": "teal",
            "hero_headline": "50,000+ TRANSFORMATIONS",
            "hero_subheadline": "⭐⭐⭐⭐⭐ 4.9/5 RATING",
            "cta": "Read Reviews",
            "bg_gradient": "from-teal-800 to-emerald-950",
            "card_accent": "teal",
            "body": "\"Within 10 days my bloating completely vanished and my energy levels are higher than in my twenties.\" Read over 50,000 verified customer stories.",
            "products": ["30-Day Gut Reset Bundle", "Daily Mineral Gel", "Digestive Sea Moss Capsules"],
            "image_url": "/static/emails/true_sea_moss/tsm_04.svg"
        },
        {
            "id": "tsm_05",
            "subject": "More energy, clearer skin, zero crash ✨",
            "preheader": "Replace synthetic multivitamins with 92 bio-available ionic minerals.",
            "badge": "Marketing",
            "date": "Sep 22, 2026",
            "time_ago": "1w",
            "full_date": "September 22, 2026 at 09:45 AM",
            "category": "Lifestyle",
            "discount": "Bundle & Save",
            "velocity": velocity,
            "theme": "green",
            "hero_headline": "MORE ENERGY",
            "hero_subheadline": "CLEARER SKIN • ZERO CRASH",
            "cta": "Start Daily Ritual",
            "bg_gradient": "from-green-700 to-emerald-900",
            "card_accent": "emerald",
            "body": "Natural energy without caffeine jitters. Sea moss contains potassium and iron that support thyroid function and cellular oxygenation.",
            "products": ["Gold Sea Moss Gel", "Chlorophyll Detox Gel", "Skin Glow Bundle"],
            "image_url": "/static/emails/true_sea_moss/tsm_05.svg"
        },
        {
            "id": "tsm_06",
            "subject": "🍁 Fall Detox Sale: Save Up To $35 Off All Jars",
            "preheader": "Stock up on seasonal immunity defenders before flu season hits.",
            "badge": "Marketing",
            "date": "Sep 20, 2026",
            "time_ago": "1w",
            "full_date": "September 20, 2026 at 11:00 AM",
            "category": "Seasonal Event",
            "discount": "Save Up To $35",
            "velocity": velocity,
            "theme": "autumn",
            "hero_headline": "FALL DETOX SALE",
            "hero_subheadline": "SAVE UP TO $35 OFF",
            "cta": "Save Up To $35",
            "bg_gradient": "from-amber-800 to-stone-900",
            "card_accent": "amber",
            "body": "Prepare your immune system for cold weather. Elderberry and Gold sea moss jars marked down for 72 hours only.",
            "products": ["Fall Immunity Stack", "Elderberry Syrup + Gel", "Raw Moss 2-Pack"],
            "image_url": "/static/emails/true_sea_moss/tsm_06.svg"
        },
        {
            "id": "tsm_07",
            "subject": "🌊 Wildcrafted in St. Lucia: Why Raw Marine Sea Moss Wins",
            "preheader": "Sun-dried on volcanic rocks, washed with clean limestone spring water.",
            "badge": "Marketing",
            "date": "Sep 17, 2026",
            "time_ago": "1w",
            "full_date": "September 17, 2026 at 08:30 AM",
            "category": "Brand Story",
            "discount": "Pure Harvest",
            "velocity": velocity,
            "theme": "blue",
            "hero_headline": "PRISTINE ST. LUCIA",
            "hero_subheadline": "OCEAN-FED WILDCRAFTED",
            "cta": "Our Harvest Story",
            "bg_gradient": "from-blue-900 to-slate-950",
            "card_accent": "blue",
            "body": "Never pool-grown. Our Chondrus Crispus and Eucheuma Cottonii are harvested by generational divers in the protected marine waters of St. Lucia.",
            "products": ["St. Lucia Raw Wildcrafted Moss", "Sun-Dried Gold Moss", "Purple Marine Moss"],
            "image_url": "/static/emails/true_sea_moss/tsm_07.svg"
        },
        {
            "id": "tsm_08",
            "subject": "🥄 2 Tablespoons Daily: Your 30-Day Gut Reset Guide",
            "preheader": "Blend in smoothies, tea, or take straight from the spoon every morning.",
            "badge": "Marketing",
            "date": "Sep 15, 2026",
            "time_ago": "2w",
            "full_date": "September 15, 2026 at 07:15 AM",
            "category": "Routine Guide",
            "discount": "Free Recipe Book",
            "velocity": velocity,
            "theme": "emerald",
            "hero_headline": "2 TABLESPOONS DAILY",
            "hero_subheadline": "YOUR 30-DAY RESET",
            "cta": "Join The Reset",
            "bg_gradient": "from-emerald-900 to-black",
            "card_accent": "emerald",
            "body": "How to make sea moss a seamless part of your morning: blend 2 tablespoons into your daily coffee, smoothie, or oatmeal.",
            "products": ["Morning Routine Bundle", "Gold Gel Jar 16oz", "Bamboo Serving Spoon"],
            "image_url": "/static/emails/true_sea_moss/tsm_08.svg"
        },
        {
            "id": "tsm_09",
            "subject": "🛡️ VIP Early Access: Immunity Shield Elderberry + Zinc 30% OFF",
            "preheader": "Exclusive early bird VIP pricing unlocked for subscribers only.",
            "badge": "VIP Access",
            "date": "Sep 13, 2026",
            "time_ago": "2w",
            "full_date": "September 13, 2026 at 06:00 PM",
            "category": "VIP Secret",
            "discount": "30% Off VIP",
            "velocity": velocity,
            "theme": "indigo",
            "hero_headline": "IMMUNITY SHIELD",
            "hero_subheadline": "ELDERBERRY + ZINC 30% OFF",
            "cta": "Unlock 30% Off",
            "bg_gradient": "from-indigo-900 to-purple-950",
            "card_accent": "indigo",
            "body": "Our most requested formula is officially restocked. Sea moss gel infused with wild European elderberry, ginger root, and bio-chelated zinc.",
            "products": ["Immunity Shield Elderberry Gel", "Zinc Mineral Drops", "Immune Tea Blend"],
            "image_url": "/static/emails/true_sea_moss/tsm_09.svg"
        },
        {
            "id": "tsm_10",
            "subject": "⚡ 48-Hour Flash Sale: $15 OFF Superfood Gummies",
            "preheader": "Pectin-based, non-GMO, vegan gummies with Irish Moss, Bladderwrack & Burdock.",
            "badge": "Flash Sale",
            "date": "Sep 11, 2026",
            "time_ago": "2w",
            "full_date": "September 11, 2026 at 11:20 AM",
            "category": "Flash Sale",
            "discount": "$15 Off",
            "velocity": velocity,
            "theme": "rose",
            "hero_headline": "$15 OFF GUMMIES",
            "hero_subheadline": "DAILY CHEWABLE SUPERFOOD",
            "cta": "Shop Gummies",
            "bg_gradient": "from-pink-900 to-rose-950",
            "card_accent": "rose",
            "body": "Don't like the texture of gel? Grab our chewable raspberry & passionfruit gummies with the exact same 92 minerals in 2 delicious daily bites.",
            "products": ["Sea Moss Gummy Jar (60ct)", "Gummy 3-Pack Bundle", "Kids Mineral Gummies"],
            "image_url": "/static/emails/true_sea_moss/tsm_10.svg"
        },
        {
            "id": "tsm_11",
            "subject": "📦 Bundle & Save 40%: The 3-Jar Power Trio",
            "preheader": "Gold Sea Moss + Elderberry Defense + Chlorophyll Detox Gel in one box.",
            "badge": "Marketing",
            "date": "Sep 9, 2026",
            "time_ago": "2w",
            "full_date": "September 9, 2026 at 10:00 AM",
            "category": "Value Bundle",
            "discount": "Save 40%",
            "velocity": velocity,
            "theme": "teal",
            "hero_headline": "BUNDLE & SAVE 40%",
            "hero_subheadline": "THE 3-JAR POWER TRIO",
            "cta": "Get The Trio",
            "bg_gradient": "from-teal-900 to-stone-900",
            "card_accent": "teal",
            "body": "The ultimate full-spectrum wellness protocol. Morning energy with Gold, afternoon detox with Chlorophyll, and evening immune defense with Elderberry.",
            "products": ["Power Trio Bundle", "Cold-Pack Storage Box", "Recipe E-Book"],
            "image_url": "/static/emails/true_sea_moss/tsm_11.svg"
        },
        {
            "id": "tsm_12",
            "subject": "🔄 Subscribe & Save 25% + Free Expedited Cold Shipping",
            "preheader": "Never run out. Swap flavors, pause or cancel anytime with 1 click.",
            "badge": "Marketing",
            "date": "Sep 7, 2026",
            "time_ago": "3w",
            "full_date": "September 7, 2026 at 02:00 PM",
            "category": "Subscription",
            "discount": "25% Off Auto-Ship",
            "velocity": velocity,
            "theme": "sky",
            "hero_headline": "SUBSCRIBE & SAVE 25%",
            "hero_subheadline": "+ FREE EXPEDITED COLD SHIPPING",
            "cta": "Activate Refills",
            "bg_gradient": "from-sky-900 to-slate-900",
            "card_accent": "sky",
            "body": "Put your health on auto-pilot. Monthly subscribers get locked-in 25% savings, VIP early access to all new flavor drops, and free thermal box delivery.",
            "products": ["Monthly Auto-Ship Gel", "Bi-Weekly Fresh Gel Refill", "Custom Flavor Mix"],
            "image_url": "/static/emails/true_sea_moss/tsm_12.svg"
        },
        {
            "id": "tsm_13",
            "subject": "🌾 Back In Stock: Raw Gold Irish Moss (Make Gel at Home)",
            "preheader": "16oz Sun-dried raw marine moss makes up to 8 jars of fresh sea moss gel.",
            "badge": "Marketing",
            "date": "Sep 4, 2026",
            "time_ago": "3w",
            "full_date": "September 4, 2026 at 10:15 AM",
            "category": "Restock",
            "discount": "Restock Alert",
            "velocity": velocity,
            "theme": "amber",
            "hero_headline": "RAW GOLD IRISH MOSS",
            "hero_subheadline": "MAKE YOUR OWN GEL AT HOME",
            "cta": "Get Raw Moss",
            "bg_gradient": "from-amber-900 to-yellow-950",
            "card_accent": "amber",
            "body": "Love crafting your own DIY wellness recipes? Our 100% pure sun-dried raw sea moss is back in stock. Simply soak with lime, blend with spring water, and enjoy.",
            "products": ["16oz Raw Gold Irish Moss", "32oz Bulk Wildcrafted Pouch", "High-Speed Gel Blender Kit"],
            "image_url": "/static/emails/true_sea_moss/tsm_13.svg"
        },
        {
            "id": "tsm_14",
            "subject": "🧬 Did you know? 92 of 102 minerals your body needs",
            "preheader": "Rich in Iodine, Potassium, Calcium, Sulfur, Iron, Silica & B-Complex vitamins.",
            "badge": "Marketing",
            "date": "Aug 31, 2026",
            "time_ago": "4w",
            "full_date": "August 31, 2026 at 09:00 AM",
            "category": "Educational",
            "discount": "Free Wellness Guide",
            "velocity": velocity,
            "theme": "green",
            "hero_headline": "92 OF 102 MINERALS",
            "hero_subheadline": "WHY YOUR BODY CRAVES IT",
            "cta": "Learn The Science",
            "bg_gradient": "from-emerald-950 to-slate-900",
            "card_accent": "emerald",
            "body": "Modern soils are depleted of essential trace minerals. Just 2 tablespoons of wildcrafted marine sea moss provides bio-available minerals that synthetic pills can't match.",
            "products": ["Mineral Deficiency Guide", "Gold Sea Moss Gel", "Irish Moss Powder"],
            "image_url": "/static/emails/true_sea_moss/tsm_14.svg"
        },
        {
            "id": "tsm_15",
            "subject": "🌸 Sea Moss + Marine Collagen: The Ultimate Skin Elixir",
            "preheader": "Marine collagen peptides blended with sea moss for youthful skin elasticity.",
            "badge": "Marketing",
            "date": "Aug 27, 2026",
            "time_ago": "4w",
            "full_date": "August 27, 2026 at 11:30 AM",
            "category": "Beauty Drop",
            "discount": "Launch 20% Off",
            "velocity": velocity,
            "theme": "rose",
            "hero_headline": "SEA MOSS + COLLAGEN",
            "hero_subheadline": "HAIR, SKIN & NAILS ELIXIR",
            "cta": "Glow From Within",
            "bg_gradient": "from-pink-900 to-purple-950",
            "card_accent": "pink",
            "body": "Nourish your skin from the inside out. Plant sulfur in sea moss pairs synergistically with marine collagen peptides to promote natural collagen synthesis.",
            "products": ["Sea Moss Collagen Glow Gel", "Collagen Peptide Powder", "Hydrating Facial Mist"],
            "image_url": "/static/emails/true_sea_moss/tsm_15.svg"
        },
        {
            "id": "tsm_16",
            "subject": "🎁 FLASH SALE: Buy 2 Get 1 FREE Sitewide",
            "preheader": "Add any 3 products to cart. Lowest priced item automatically free.",
            "badge": "Flash Sale",
            "date": "Aug 24, 2026",
            "time_ago": "1mo",
            "full_date": "August 24, 2026 at 10:00 AM",
            "category": "Flash Sale",
            "discount": "Buy 2 Get 1 Free",
            "velocity": velocity,
            "theme": "red",
            "hero_headline": "BUY 2 GET 1 FREE",
            "hero_subheadline": "MIX & MATCH ALL FLAVORS",
            "cta": "Mix & Match",
            "bg_gradient": "from-red-900 to-stone-900",
            "card_accent": "red",
            "body": "48 hours only! Stock your fridge with fresh flavors. Mix and match between Gold, Elderberry, Dragonfruit, and Superfood Gummies.",
            "products": ["Mix & Match Trio", "Elderberry Immune Gel", "Raw Moss 16oz"],
            "image_url": "/static/emails/true_sea_moss/tsm_16.svg"
        },
        {
            "id": "tsm_17",
            "subject": "📱 Why 100,000+ Health Enthusiasts Swapped Multi-Vitamins",
            "preheader": "#TrueSeaMoss has over 45.4M views on TikTok. Here is why it's viral.",
            "badge": "Marketing",
            "date": "Aug 20, 2026",
            "time_ago": "1mo",
            "full_date": "August 20, 2026 at 03:00 PM",
            "category": "Social Proof",
            "discount": "Starter Bundle 25% Off",
            "velocity": velocity,
            "theme": "slate",
            "hero_headline": "WHY 100K+ SWITCHED",
            "hero_subheadline": "#TRUESEAMOSS 45.4M VIEWS",
            "cta": "Watch Reviews",
            "bg_gradient": "from-slate-900 to-black",
            "card_accent": "sky",
            "body": "Viral TikTok creator recipes, before-and-after skin journeys, and gut health transformations. Discover why this simple sea plant is taking over wellness.",
            "products": ["Viral TikTok Starter Kit", "Smoothie Recipe Cards", "Gold Gel Jar"],
            "image_url": "/static/emails/true_sea_moss/tsm_17.svg"
        },
        {
            "id": "tsm_18",
            "subject": "⏰ FINAL HOURS: Free Priority Cold-Pack Shipping Ending Tonight!",
            "preheader": "Temperature-controlled insulated shipping free on all orders placed today.",
            "badge": "Marketing",
            "date": "Aug 16, 2026",
            "time_ago": "1mo",
            "full_date": "August 16, 2026 at 05:00 PM",
            "category": "Shipping Promo",
            "discount": "Free Cold-Pack Shipping",
            "velocity": velocity,
            "theme": "violet",
            "hero_headline": "FINAL HOURS",
            "hero_subheadline": "FREE COLD-PACK DELIVERY",
            "cta": "Claim Free Shipping",
            "bg_gradient": "from-violet-900 to-black",
            "card_accent": "violet",
            "body": "Never worry about spoiled gel. Our eco-friendly thermal cold packaging ensures your sea moss arrives chilled, fresh, and ready for your fridge.",
            "products": ["Thermal Insulated Shipping Pack", "Gold Sea Moss Gel", "2-Pack Bundle"],
            "image_url": "/static/emails/true_sea_moss/tsm_18.svg"
        }
    ]

    return {
        "brand": "True Sea Moss",
        "domain": "trueseamoss.com",
        "total_emails": total_emails,
        "velocity": "3.8/wk",
        "provider": "Klaviyo",
        "sub_tabs": ["Email Library", "Insights", "Calendar", "Flows"],
        "campaigns": campaigns,
        "insights": {
            "avg_weekly_sends": 3.8,
            "best_send_day": "Monday & Wednesday",
            "best_send_time": "09:00 AM EST",
            "promo_ratio": 65,
            "educational_ratio": 35,
            "avg_discount": "20% - 35% OFF",
            "top_subject_keywords": ["Minerals", "BOGO", "Free", "Detox", "Gut Health", "Wildcrafted"]
        }
    }

def generate_dynamic_dataset(brand_name: str) -> dict:
    """Generate intelligent, industry-specific email campaigns for any arbitrary brand."""
    slug = slugify(brand_name)
    brand_dir = os.path.join(STATIC_EMAILS_DIR, slug)
    os.makedirs(brand_dir, exist_ok=True)

    # Detect brand niche
    lower = brand_name.lower()
    is_apparel = any(w in lower for w in ["apparel", "wear", "shirt", "clothing", "hoodie", "fashion", "boutique"])
    is_health = any(w in lower for w in ["health", "moss", "tea", "supp", "herb", "keto", "vital", "glow", "skin", "body"])
    is_edc = any(w in lower for w in ["ridge", "wallet", "tactical", "tool", "knife", "gear", "pack", "bag"])
    is_baby = any(w in lower for w in ["baby", "mom", "kid", "cozy", "nurse", "pump", "child"])

    niche = "Bestsellers"
    hero_item = "Exclusive Collection"
    category = "Brand Essentials"
    cadence = "3.2/wk"
    total_emails = 96

    if is_edc:
        niche = "Everyday Carry & Wallets"
        hero_item = "Minimalist RFID Wallet"
        category = "EDC Gear"
        cadence = "2.9/wk"
        total_emails = 112
    elif is_baby:
        niche = "Maternity & Baby Essentials"
        hero_item = "Hands-Free Wearable Pump"
        category = "Maternity Comfort"
        cadence = "3.5/wk"
        total_emails = 135
    elif is_health:
        niche = "Clean Wellness & Superfoods"
        hero_item = "Daily Mineral Formula"
        category = "Superfood Health"
        cadence = "3.8/wk"
        total_emails = 124
    elif is_apparel:
        niche = "Comfort Apparel & Loungewear"
        hero_item = "Signature Soft Robe"
        category = "Loungewear"
        cadence = "4.0/wk"
        total_emails = 160

    campaigns = [
        {
            "id": f"{slug}_01",
            "subject": f"🔥 New Release: The {brand_name} {hero_item} is here",
            "preheader": f"Crafted with premium materials. Experience the newest innovation from {brand_name}.",
            "badge": "Marketing",
            "date": "Sep 29, 2026",
            "time_ago": "1d",
            "full_date": "September 29, 2026 at 10:00 AM",
            "category": "Product Launch",
            "discount": "New Release",
            "velocity": cadence,
            "theme": "slate",
            "hero_headline": f"MEET THE NEW {brand_name.upper()}",
            "hero_subheadline": hero_item.upper(),
            "cta": "Shop The Drop",
            "body": f"Engineered for daily performance. Discover our latest release designed specifically for your lifestyle.",
            "products": [f"{brand_name} {hero_item}", f"{brand_name} Pro Bundle", f"{brand_name} Travel Kit"]
        },
        {
            "id": f"{slug}_02",
            "subject": f"⚡ FLASH SALE: Buy 1 Get 1 50% Off Everything!",
            "preheader": f"48 hours only. Mix & match across all {brand_name} bestsellers.",
            "badge": "Flash Sale",
            "date": "Sep 27, 2026",
            "time_ago": "3d",
            "full_date": "September 27, 2026 at 11:30 AM",
            "category": "Flash Sale",
            "discount": "BOGO 50% Off",
            "velocity": cadence,
            "theme": "indigo",
            "hero_headline": "BUY 1 GET 1 50% OFF",
            "hero_subheadline": "SITEWIDE 48H FLASH",
            "cta": "Claim Your Deal",
            "body": f"Double up on your favorites. Add any two products to cart and get the second for half price.",
            "products": [f"{brand_name} Essential Pack", f"{brand_name} Deluxe Set", f"{brand_name} Gift Card"]
        },
        {
            "id": f"{slug}_03",
            "subject": f"⭐ Over 25,000 5-Star Reviews: Here is why customers love us",
            "preheader": f"Real feedback from verified {brand_name} buyers worldwide.",
            "badge": "Marketing",
            "date": "Sep 25, 2026",
            "time_ago": "5d",
            "full_date": "September 25, 2026 at 09:15 AM",
            "category": "Social Proof",
            "discount": "Free Shipping",
            "velocity": cadence,
            "theme": "emerald",
            "hero_headline": "25,000+ FIVE-STAR REVIEWS",
            "hero_subheadline": "⭐⭐⭐⭐⭐ VERIFIED SATISFACTION",
            "cta": "Read Customer Stories",
            "body": f"Don't just take our word for it. See why over 25,000 customers rate {brand_name} 4.9/5 stars.",
            "products": [f"{brand_name} Bestseller #1", f"{brand_name} Top Rated Pack", f"{brand_name} Starter Set"]
        },
        {
            "id": f"{slug}_04",
            "subject": f"🖤 VIP Early Access: Secret Fall Vault Unlocked",
            "preheader": f"Shhh! You're on our VIP list. Enjoy exclusive 30% savings before anyone else.",
            "badge": "VIP Access",
            "date": "Sep 24, 2026",
            "time_ago": "6d",
            "full_date": "September 24, 2026 at 06:00 PM",
            "category": "VIP Secret",
            "discount": "VIP 30% Off",
            "velocity": cadence,
            "theme": "purple",
            "hero_headline": "VIP ACCESS ONLY",
            "hero_subheadline": "SECRET 30% OFF VAULT",
            "cta": "Unlock VIP Sale",
            "body": f"As an email subscriber, unlock private access to our seasonal vault with extra savings applied at checkout.",
            "products": [f"{brand_name} VIP Mystery Box", f"{brand_name} Limited Edition", f"{brand_name} Pro Bundle"]
        },
        {
            "id": f"{slug}_05",
            "subject": f"📦 Subscribe & Save 20% + Free Express Shipping Every Month",
            "preheader": f"Never run out of your daily essentials from {brand_name}.",
            "badge": "Marketing",
            "date": "Sep 22, 2026",
            "time_ago": "1w",
            "full_date": "September 22, 2026 at 08:30 AM",
            "category": "Subscription",
            "discount": "20% Off Monthly",
            "velocity": cadence,
            "theme": "sky",
            "hero_headline": "SUBSCRIBE & SAVE 20%",
            "hero_subheadline": "+ FREE SHIPPING FOR LIFE",
            "cta": "Activate Subscription",
            "body": f"Flexible auto-ship with zero commitments. Pause, swap products, or cancel anytime with one click.",
            "products": [f"{brand_name} Monthly Refill", f"{brand_name} Bi-Weekly Pack", f"{brand_name} Family Bundle"]
        },
        {
            "id": f"{slug}_06",
            "subject": f"🎁 Seasonal Markdown: Save Up To $40 Today",
            "preheader": f"Our biggest seasonal price drop is officially live. Limited quantities available.",
            "badge": "Marketing",
            "date": "Sep 20, 2026",
            "time_ago": "1w",
            "full_date": "September 20, 2026 at 10:00 AM",
            "category": "Seasonal Event",
            "discount": "Up to $40 Off",
            "velocity": cadence,
            "theme": "amber",
            "hero_headline": "SEASONAL MARKDOWN",
            "hero_subheadline": "SAVE UP TO $40 TODAY",
            "cta": "Shop The Sale",
            "body": f"Score bestselling comfort and utility with up to $40 off selected styles. Available while stock lasts.",
            "products": [f"{brand_name} Seasonal Stack", f"{brand_name} Classic Pack", f"{brand_name} Gift Duo"]
        },
        {
            "id": f"{slug}_07",
            "subject": f"⏰ FINAL HOURS: Free Worldwide Express Shipping Ends Tonight",
            "preheader": f"Order before midnight to receive guaranteed priority courier delivery.",
            "badge": "Marketing",
            "date": "Sep 17, 2026",
            "time_ago": "1w",
            "full_date": "September 17, 2026 at 04:30 PM",
            "category": "Shipping Promo",
            "discount": "Free Express Shipping",
            "velocity": cadence,
            "theme": "violet",
            "hero_headline": "FINAL HOURS",
            "hero_subheadline": "FREE EXPRESS SHIPPING",
            "cta": "Claim Free Delivery",
            "body": f"We're upgrading all standard shipping to DHL Express at no cost on orders placed before midnight.",
            "products": [f"{brand_name} Core Kit", f"{brand_name} Carry Bag", f"{brand_name} Accessories"]
        },
        {
            "id": f"{slug}_08",
            "subject": f"🌿 Why Quality Matters: The {brand_name} Difference",
            "preheader": f"Behind the scenes of our ethical manufacturing and design philosophy.",
            "badge": "Marketing",
            "date": "Sep 15, 2026",
            "time_ago": "2w",
            "full_date": "September 15, 2026 at 09:00 AM",
            "category": "Brand Story",
            "discount": "Sustainable Sourcing",
            "velocity": cadence,
            "theme": "teal",
            "hero_headline": "THE DIFFERENCE",
            "hero_subheadline": "CRAFTED WITHOUT COMPROMISE",
            "cta": "Discover Our Story",
            "body": f"Every {brand_name} product is rigorously tested for durability, sustainability, and peak real-world performance.",
            "products": [f"{brand_name} Eco Collection", f"{brand_name} Signature Edition", f"{brand_name} Lifetime Warranty"]
        }
    ]

    # Generate SVGs for this brand
    for idx, c in enumerate(campaigns):
        svg_filename = f"{slug}_{idx+1:02d}.svg"
        svg_path = os.path.join(brand_dir, svg_filename)
        c["image_url"] = f"/static/emails/{slug}/{svg_filename}"

        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 800" width="600" height="800">
  <defs>
    <linearGradient id="grad_{idx}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
  </defs>
  <rect width="600" height="800" fill="url(#grad_{idx})" rx="24"/>
  <circle cx="500" cy="150" r="180" fill="#3b82f6" opacity="0.1"/>
  <circle cx="100" cy="650" r="160" fill="#10b981" opacity="0.08"/>
  <g transform="translate(50, 45)">
    <text x="0" y="24" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="16" font-weight="900" fill="#ffffff" letter-spacing="1">{brand_name.upper()}</text>
    <text x="500" y="24" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="600" fill="#94a3b8" text-anchor="end">{category}</text>
  </g>
  <g transform="translate(50, 110)">
    <rect width="140" height="28" rx="14" fill="#2563eb"/>
    <text x="70" y="19" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="800" fill="#ffffff" text-anchor="middle">{c['badge']}</text>
  </g>
  <text x="50" y="190" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="32" font-weight="900" fill="#ffffff">{c['hero_headline']}</text>
  <text x="50" y="225" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="20" font-weight="800" fill="#60a5fa">{c['hero_subheadline']}</text>
  <g transform="translate(50, 260)">
    <rect width="500" height="340" rx="20" fill="#ffffff" opacity="0.06" stroke="#ffffff" stroke-opacity="0.12" stroke-width="1.5"/>
    <circle cx="250" cy="150" r="80" fill="#3b82f6" opacity="0.2"/>
    <text x="250" y="140" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="48" text-anchor="middle">✨</text>
    <text x="250" y="180" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="18" font-weight="800" fill="#ffffff" text-anchor="middle">{hero_item}</text>
    <text x="250" y="205" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="12" font-weight="600" fill="#94a3b8" text-anchor="middle">Official {brand_name} Campaign</text>
    <text x="250" y="280" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="13" font-weight="600" fill="#cbd5e1" text-anchor="middle">{c['body'][:80]}...</text>
  </g>
  <g transform="translate(150, 640)">
    <rect width="300" height="56" rx="28" fill="#3b82f6"/>
    <text x="150" y="34" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="14" font-weight="900" fill="#ffffff" text-anchor="middle" letter-spacing="1">{c['cta']} →</text>
  </g>
  <text x="300" y="740" font-family="-apple-system, BlinkMacSystemFont, sans-serif" font-size="11" font-weight="500" fill="#64748b" text-anchor="middle">{brand_name} Official Newsletters • Sent via Klaviyo</text>
</svg>'''
        try:
            with open(svg_path, "w", encoding="utf-8") as f:
                f.write(svg_content)
        except Exception:
            pass

    return {
        "brand": brand_name,
        "domain": f"{slug}.com",
        "total_emails": total_emails,
        "velocity": cadence,
        "provider": "Klaviyo",
        "sub_tabs": ["Email Library", "Insights", "Calendar", "Flows"],
        "campaigns": campaigns,
        "insights": {
            "avg_weekly_sends": float(cadence.split("/")[0]),
            "best_send_day": "Tuesday & Thursday",
            "best_send_time": "10:00 AM",
            "promo_ratio": 70,
            "educational_ratio": 30,
            "avg_discount": "20% - 30% OFF",
            "top_subject_keywords": ["Drop", "Save", "Free", "Sale", "New", "Limited"]
        }
    }

def get_emails_data(brand_name: str, force_refresh: bool = False) -> dict:
    """Retrieve or generate brand-specific email campaigns with cache control."""
    slug = slugify(brand_name)
    cache_path = os.path.join(CACHE_DIR, f"email_{slug}.json")

    # If force refresh, delete cache file
    if force_refresh and os.path.exists(cache_path):
        try:
            os.remove(cache_path)
            print(f"[EmailScanner] Purged stale email cache for: {brand_name}")
        except Exception as e:
            print(f"[EmailScanner] Error removing cache: {e}")

    # Return cached data if available and not forced
    if not force_refresh and os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    # Generate brand-tailored dataset
    lower = brand_name.lower().strip()
    if "oodie" in lower:
        data = generate_oodie_dataset()
    elif "sea moss" in lower or "seamoss" in lower or "creatine" in lower:
        data = generate_true_sea_moss_dataset()
    else:
        data = generate_dynamic_dataset(brand_name)

    # Save to cache
    try:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[EmailScanner] Cache save error: {e}")

    return data

if __name__ == "__main__":
    oodie = get_emails_data("The Oodie", force_refresh=True)
    tsm = get_emails_data("True sea moss", force_refresh=True)
    print(f"Oodie campaigns: {len(oodie['campaigns'])}, Card 1: {oodie['campaigns'][0]['subject']}")
    print(f"True sea moss campaigns: {len(tsm['campaigns'])}, Card 1: {tsm['campaigns'][0]['subject']}")
