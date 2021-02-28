from PIL import ImageColor
from src.tints.utils.color import compare_delta_e,get_dominant_color
from src.tints.models.lipstick import Lipstick
from src.tints.settings import APP_INPUT,APP_OUTPUT, COLOR_COMPARE_VAL, METHOD_NUM, RETURN_SIZE

# Contain all lipstick function

def print_result(number, lip_list):
    print()
    if(len(lip_list) <= number):
        for i in range(len(lip_list)):
            print("Brand = {}, Color name = {}, RGB = {}, DeltaE = {}".format(lip_list[i]["brand"],lip_list[i]["color_name"],lip_list[i]["rgb_value"], lip_list[i]["deltaE"]))
    else:
        for i in range(number):
            print("Brand = {}, Color name = {}, RGB = {}, DeltaE = {}".format(lip_list[i]["brand"],lip_list[i]["color_name"],lip_list[i]["rgb_value"], lip_list[i]["deltaE"]))
    print()

def get_lipstick (dominant_color_list, brand_list):
    similar_lipstick = [] # for append similar lipstick
    for dominant_color in dominant_color_list:
        for brand_name in brand_list:
            lipstick_list = Lipstick.find_lipstick_by_brand(brand_name)
            for serie in lipstick_list:
                for color in serie['product_colors']:
                    rgb_color = ImageColor.getcolor(color['hex_value'], "RGB")
                    str_rgb_color = str(rgb_color)
                    # Compare using delta_e
                    compare_result = compare_delta_e(dominant_color, rgb_color)
                    if(compare_result <= COLOR_COMPARE_VAL):
                            similar_lipstick.append({'_id':serie['_id'],'brand':brand_name,'serie':serie['name'],'price':serie['price'],'image_link':serie['image_link'],'product_link':serie['product_link'],'category':serie['category'],'color_name':color['colour_name'],'rgb_value':str_rgb_color, 'deltaE':compare_result, 'api_image_link': serie['api_featured_image']})
        if not similar_lipstick:
            break
    if len(similar_lipstick) >= RETURN_SIZE:
        similar_lipstick = similar_lipstick[:RETURN_SIZE]
    else:
        similar_lipstick = similar_lipstick[:len(similar_lipstick)]
    similar_lipstick.sort(key=lambda x: x.get('deltaE'))
    # Print for check return lip color easeier
    print_result(5,similar_lipstick)
    return similar_lipstick

def predict_lipstick_color(userID):    
    dominant_color_list = get_dominant_color(APP_OUTPUT,userID)
    print("Dominant color list=",dominant_color_list)
    brand_list = Lipstick.distinct_brand()
    return get_lipstick(dominant_color_list, brand_list)

# if __name__ == "__main__":
#     predict_lipstick_color()