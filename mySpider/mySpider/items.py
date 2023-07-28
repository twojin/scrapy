# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


# class MyspiderItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass


class DoubanBookItem(Item):

    table = "douban_book"
    title = Field()
    author = Field()
    translator = Field()
    introduction = Field()
    kind = Field()
    wordCount = Field()
    originalPrice = Field()
    discountPrice = Field()

class BilibiliUserItem(Item):
    table = "bilibili_user"
    mid2 = "mid"
    name2 = "name"
    sex2 = "sex"
    sign2 = "sign"
    rank2 = "rank"
    level2 = "level"
    silence2 = "silence"
    official_role2 = "official_role"
    official_type2 = "official_type"
    vip_type2 = "vip_type"
    vip_status2 = "vip_status"
    vip_due_date2 = "vip_due_date"
    vip_label_text2 = "vip_label_text"
    vip_label_label_theme2 = "vip_label_label_theme"
    vip_role2 = "vip_role"
    vip_tv_vip_status2 = "vip_tv_vip_status"
    birthday2 = "birthday"
    school_name2 = "school_name"
    is_senior_member2 = "is_senior_member"
    elec_show_info_show2 = "elec_show_info_show"
    elec_show_info_state2 = "elec_show_info_state"
    following2 = "following"
    follower2 = "follower"

    mid = Field()
    name = Field()
    sex = Field()
    sign = Field()
    rank = Field()
    level = Field()
    silence = Field()
    official_role = Field()
    official_type = Field()
    vip_type = Field()
    vip_status = Field()
    vip_due_date = Field()
    vip_label_text = Field()
    vip_label_label_theme = Field()
    vip_role = Field()
    vip_tv_vip_status = Field()
    birthday = Field()
    school_name = Field()
    is_senior_member = Field()
    elec_show_info_show = Field()
    elec_show_info_state = Field()
    following = Field()
    follower = Field()

