import gettext
import os
import traceback
from logging import warning

from thonny import get_workbench

BASE_LANGUAGE_CODE = "en_US"
BASE_LANGUAGE_NAME = "English"

# http://www.internationalphoneticalphabet.org/languages/language-names-in-native-language/

LANGUAGES_DICT = {
    "cs_CZ": "Čeština [BETA]",
    "de_DE": "Deutsch [BETA]",
    "et_EE": "Eesti",
    BASE_LANGUAGE_CODE: BASE_LANGUAGE_NAME,
    "es_ES": "Español [BETA]",
    "fr_FR": "Français [BETA]",
    "it_IT": "Italiano [BETA]",
    "nb_NO": "Norsk (Bokmål) [BETA]",
    "nn_NO": "Norsk (Nynorsk) [BETA]",
    "nl_NL": "Nederlands",
    "pl_PL": "Polski",
    "pt_PT": "Português (PT)",
    "pt_BR": "Português (BR)",
    "ro_RO": "Român [BETA]",
    "ru_RU": "Русский",
    "sv_SE": "Svenska [BETA]",
    "tr_TR": "Türkçe [BETA]",
    "uk_UA": "Українська",
    "zh_TW": "繁體中文-TW",
    "zh_CN": "简体中文 ",
    "ja_JP": "日本語  [ALPHA]",
    "lt_LT": "Lietuvių",
    "el_GR": "Ελληνικά",
}

# how many spaces to add to button caption in order to make whole text visible
BUTTON_PADDING_SIZES = {"zh_TW": 4, "zh_CN": 4, "ja_JP": 4}

_translation = gettext.NullTranslations()


def get_button_padding():
    code = get_workbench().get_option("general.language")
    if code in BUTTON_PADDING_SIZES:
        return BUTTON_PADDING_SIZES[code] * " "
    else:
        return ""


def get_language_code_by_name(name):
    for code in LANGUAGES_DICT:
        if LANGUAGES_DICT[code] == name:
            return code

    raise RuntimeError("Unknown language name '%s'" % name)


def tr(message: str) -> str:
    return _translation.gettext(message)


def set_language(language_code: str) -> None:
    global _translation
    try:
        path = os.path.join(os.path.dirname(__file__), "locale")
        _translation = gettext.translation("thonny", path, [language_code])
    except Exception:
        traceback.print_exc()
        warning("Could not set language to '%s" % language_code)
        _translation = gettext.NullTranslations()
