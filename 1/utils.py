import numpy as np
import re
import ast
import pandas as pd
from bidi.algorithm import get_display
from arabic_reshaper import reshape
import matplotlib.pyplot as plt

def major_categorizer(text):
    text = str(text)
    has_diploma = "دیپلم" in text
    has_assosiate = 'کاردانی' in text
    has_bachlor = 'کارشناسی' in text
    has_master = 'کارشناسی ارشد' in text
    has_phd = "دکتری" in text
    
    if has_diploma or has_assosiate or has_bachlor or has_master or has_phd:
        return has_diploma * "دیپلم " + has_assosiate * "کاردانی " + has_bachlor * "کارشناسی " + has_master * "کارشناسی ارشد " + has_phd * "دکتری "
    else:
        return "مدرک لازم نیست"
    
def gender_cleaner(text):
    if type(text) == float:
        return "تفاوتی ندارد"
    text = str(text)
    mapping = {
        "Men / Women": "تفاوتی ندارد",
        "Only Women": "فقط خانم",
        "Only Men": "فقط آقا",
        "Preferred Women": "ترجیحاً خانم",
        "Preferred Men":"ترجیحاً آقا"
    }
    try:
        return mapping[text]
    except Exception as e:
        return text


def salary_cleaner(text, return_min = True):
    
    if isinstance(text, str):
        nums = re.findall(r'\d+', text)
    else:
        return np.nan
    
    nums = [int(num) for num in nums]
    
    if return_min:
        return min(nums)
    else:
        return max(nums)
    
def days_per_week_refinement(text:str):
    shanbe_to_charshanbe = [
        "شنبه تا چهار شنبه",
        "شنبه تا چهارشنبه",
        "شنبه تا 4شنبه",
        "شنبه تا چهرشنبه",
        "شنبه تا چهارشنبه",
    ]
    shanbe_to_pangshanbe = {
        "شنبه تا پنج شنبه",
        "شنبه تا 5 شنبه",
        "شنبه تا پنجشنبه",
        "شنبه تاپنج شنبه",
        "شنبه تا 5شنبه",
        "شنبه تا 5شنبه"
    }
    if any([x in text for x in shanbe_to_charshanbe]):
        if "پنج شنبه" in text:
            return 6
        else:
            return 5
    elif any([x in text for x in shanbe_to_pangshanbe]):
        return 6
    elif "همه" in text:
        return 7
    else:
        return 1
    
    
def convert_digits(text):
   if not isinstance(text, str):
      return text
   mapping = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
   return text.translate(mapping)


def safe_parse_list(x):
   if pd.isna(x):
      return []
   if isinstance(x, list):
      return x
   try:
      return ast.literal_eval(x)
   except:
      return []


LANGUAGE_NORMALIZATION = {

   # English
   "انگلیسی": "English",
   "زبان انگلیسی": "English",
   "English": "English",

   # Chinese
   "چینی": "Chinese",
   "ماندارین": "Chinese",
   "Mandarin": "Chinese",
   "Chinese": "Chinese",

   # French
   "فرانسه": "French",
   "French": "French",

   # Arabic
   "عربی": "Arabic",
   "Arabic": "Arabic",

   # German
   "آلمانی": "German",
   "German": "German",

   # Turkish
   "ترکی": "Turkish",
   "Turkish": "Turkish",

   # Persian
   "فارسی": "Persian",
   "Persian": "Persian",

   # Russian
   "روسی": "Russian",
   "Russian": "Russian",

   # Japanese
   "ژاپنی": "Japanese",

   # Hindi
   "هندی": "Hindi",

   # Spanish
   "اسپانیایی": "Spanish",

   # Kurdish
   "کوردی": "Kurdish",

   # Armenian
   "ارمنی": "Armenian",

   # Italian
   "ایتالیایی": "Italian",

   # Korean
   "کره ای": "Korean",

   # Dutch
   "هلندی": "Dutch",
}


def normalize_language_name(raw):
   raw = str(raw).strip()
   raw = convert_digits(raw)

   raw = re.sub(r"\(.*?\)", "", raw).strip()

   raw = re.sub(r"(عمومی|تخصصی|محاوره‌ای|محاوره ای)", "", raw).strip()

   if raw in LANGUAGE_NORMALIZATION:
      return LANGUAGE_NORMALIZATION[raw]

   if re.match(r"[A-Za-z]+", raw):
      return raw.capitalize()

   return raw



def extract_level(item):
   item = convert_digits(item)
   m = re.search(r"(\d+)\s*[%٪]", item)
   if m:
      return int(m.group(1))
   return 0



def clean_language_column(df, colname):
   new_df = pd.DataFrame()
   new_df[colname + "_parsed"] = df[colname].apply(safe_parse_list)

   all_languages = set()

   for row in new_df[colname + "_parsed"]:
      for item in row:
            lang = item.split("|")[0].strip()
            lang = normalize_language_name(lang)
            all_languages.add(lang)

   all_languages = sorted(all_languages)

   for lang in all_languages:
      new_df[f"lang_{lang}"] = 0

   for idx, row in new_df.iterrows():
      for item in row[colname + "_parsed"]:
            try:
               raw_lang, level_text = item.split("|")
               lang = normalize_language_name(raw_lang)
               level = extract_level(level_text)
               new_df.at[idx, f"lang_{lang}"] = level
            except:
               pass

   return new_df
    
    
def business_trip_filter(text):
    negative_cases = [
        '-',
        '0',
        'ندارد',
        '_',
        '--',
        'سفر ندارد',
        'هیچ',
        'نیست',
        'نیازی نیست',
        '.',
        '-----',
        '---',
        'نیازی به سفر کاری ندارد',
        'نامشخص',
        'عدم نیاز مسافرتی'
    ]
    if text is np.nan:
        return 0
    
    for item in negative_cases:
        if text == item:
            return 0
    return 1

eng_to_fa_industry = {
    "IT / Software / Hardware": "فناوری اطلاعات / نرم افزار و سخت افزار",
    "Internet Provider / E - commerce / Online Services": "اینترنت / تجارت الکترونیک / خدمات آنلاین",
    "Consumer Goods / FMCG": "کالاهای مصرفی و تند گردش",
    "Medical Devices": "تجهیزات پزشکی",
    "Catering / Restaurant / Food and Beverage": "کترینگ / رستوران / واحدهای غذایی",
    "Travel / Hotel / Tourism": "گردشگری / هتلداری",
    "Manufacturing & Production": "تولیدی / صنعتی",
    "Pharmaceutical": "دارو",
    "Consumer Electonics / Home Appliances": "کالاهای الکتریکی و لوازم خانگی",
    "Education / Research": "آموزش / پژوهش",
    "Retail / Shopping center / Store": "خرده فروشی / مراکز خرید و فروشگاهها",
    "General Services / Contractor": "شرکت های خدماتی / پیمانکاران",
    "Finance / Investment": "سرمایه گذاری و مالی",
    "Banking": "بانکداری",
    "Oil & Gas / Petrochemical": "نفت، گاز و پتروشیمی",
    "Trading / International Affairs": "تجارت / بازرگانی",
    "Business Services / Consulting": "خدمات سازمانی / مشاوره مدیریت",
    "Charity / Non - Profit / NGO": "خیریه / موسسات غیرانتفاعی / سازمانهای مردم نهاد",
    "Broadcast / Media / Publishing": "رسانه / چاپ و نشر",
    "Airline / Aviation": "خطوط هوایی / هوانوردی",
    "Agriculture": "کشاورزی",
    "Engineering Services / Technical Services & Solutions": "خدمات مهندسی و تخصصی",
    "Technology and Innovation / VC / Accelerator": "تکنولوژی و نوآوری / سرمایه گذاری خطرپذیر / شتاب دهنده",
    "Marketing / Advertising": "بازاریابی و تبلیغات",
    "Healthcare / Medical Services": "خدمات درمانی و سلامتی",
    "Automotive": "خودرو و صنایع وابسته",
    "Insurance": "بیمه",
    "Fashion / Luxury Goods": "مد و کالاهای لوکس",
    "Law and Legal": "حقوقی و قضایی",
    "Construction / Building Materials & Equipment": "ساخت / مصالح و تجهیزات ساختمانی",
    "Games and Entertainment": "بازی و سرگرمی",
    "Architecture": "معماری",
    "Transportation / Logistics": "حمل و نقل / ترابری",
    "Telecom": "تلکام",
}

def normalize_industry(text):
    if isinstance(text, float) and np.isnan(text):
        return []

    text = str(text).strip()

    # Replace English labels with Persian
    for eng, fa in eng_to_fa_industry.items():
        if eng.lower() in text.lower():
            text = text.replace(eng, fa)

    # Unified separators
    text = text.replace("،", "/").replace(",", "/")

    # Split
    parts = re.split(r"/|\|", text)

    # Cleanup
    cleaned = []
    for p in parts:
        p = p.strip()
        p = re.sub(r'\s+', ' ', p)

        if len(p) > 1:
            cleaned.append(p)

    # Deduplicate
    cleaned = list(dict.fromkeys(cleaned))

    return cleaned
 
 
def generate_one_hot_industry(df, col="industry"):
   new_df = pd.DataFrame()
   new_df["industry_list"] = df[col].apply(normalize_industry)

   all_tags = sorted({tag for tags in new_df["industry_list"] for tag in tags})

   # Create columns
   for tag in all_tags:
      new_df[f"ind_{tag}"] = new_df["industry_list"].apply(lambda x: int(tag in x))

   return new_df



bonus_normalizer = {
    "Bonus": "پاداش",
    "Breakfast": "صبحانه",
    "Coffee shop": "کافی شاپ",
    "Commision": "پورسانت",
    "Employee stock ownership": "سهام تشویقی",
    "Flexible working hours": "ساعت کاری منعطف",
    "Game room": "اتاق بازی",
    "Gym facilities": "امکانات ورزشی",
    "Health insurance": "بیمه درمان تکمیلی",
    "Housing": "محل سکونت سازمانی",
    "Learning stipends": "کمک هزینه دوره آموزشی",
    "Library": "کتابخانه",
    "Loan": "وام",
    "Lunch": "ناهار",
    "Military Service Option": "امریه\u200cی سربازی",
    "Occasional packages and gifts": "بسته ها و هدایای مناسبتی",
    "Parking space": "پارکینگ",
    "Purchasing coupon": "بن خرید",
    "Recreational accommodation": "اقامتگاه تفریحی",
    "Recreational and tourism facilities": "تسهیلات تفریحی و گردشگری",
    "Resting space": "فضای استراحت",
    "Snacks": "میان وعده",
    "Transportation": "سرویس رفت و برگشت",
    "House Medical doctor": "پزشک سازمانی",
    "In": "پاداش",
}

def normalize_bonus(text):
    if isinstance(text, float) and np.isnan(text):
        return []

    text = str(text).strip()

    # Replace English labels with Persian
    for eng, fa in bonus_normalizer.items():
        if eng.lower() in text.lower() and fa:
            text = text.replace(eng, fa)

    # Split
    parts = re.split(r"-", text)

    # Cleanup
    cleaned = []
    for p in parts:
        p = p.strip()
        p = re.sub(r'\s+', ' ', p)

        if len(p) > 1:
            cleaned.append(p)

    # Deduplicate
    cleaned = list(dict.fromkeys(cleaned))

    return cleaned

def generate_one_hot_bonus(df, col="bonus"):
   new_df = pd.DataFrame()
   new_df["bonus_list"] = df[col].apply(normalize_bonus)

   all_tags = sorted({tag for tags in new_df["bonus_list"] for tag in tags if tag is not np.nan})

   # Create columns
   for tag in all_tags:
      new_df[f"bonus_{tag}"] = new_df["bonus_list"].apply(lambda x: int(tag in x))

   return new_df


def plot_top_k_pie_chrt(df,column_name,title,persian=True,k=5,figsize=(7, 7),contain_rest=True):
    if isinstance(df,pd.Series):
        counts = df.value_counts()
    else:
        counts  = df[column_name].value_counts()
    top_vals = counts.head(k)
    if contain_rest:
        other_sum = counts[k:].sum()
        vals_for_plot = pd.concat([top_vals, pd.Series({"بقیه": other_sum})])
    else:
        vals_for_plot = top_vals
    if persian:
        labels = [get_display(reshape(label)) for label in vals_for_plot.index]
    else:
        labels = vals_for_plot.index
        
    plt.figure(figsize=figsize)
    plt.pie(vals_for_plot, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(title, fontsize=14)
    plt.show()
    
    
def clean_software_column(df, colname):
   level_dict = {
       "مقدماتی": 1,
       "basic": 1,
       'متوسط': 2,
       'intermediate':2,
       "پیشرفته":3,
       "advanced":3,
   } 
   new_df = pd.DataFrame(dtype=object)
   new_df[colname + "_parsed"] = df[colname].apply(safe_parse_list)

   all_softwares = set()

   for row in new_df[colname + "_parsed"]:
      for item in row:
            software = item.split("|")[0].strip()
            all_softwares.add(software)

   all_softwares = sorted(all_softwares)

   for software in all_softwares:
      new_df[f"software_{software}"] = 0

   for idx, row in new_df.iterrows():
      for item in row[colname + "_parsed"]:
            try:
               raw_software, level_text = item.split("|")
               software = raw_software.strip()
               level_text = level_text.strip().lower()
               new_df.at[idx, f"software_{software}"] = level_dict[level_text]
            except:
               pass

   return new_df

def military_service_cleaner(text: str):
   if text is np.nan:
      return "مهم نیست"
   else:
      return "الزامی"
  
