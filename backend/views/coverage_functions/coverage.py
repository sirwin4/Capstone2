#if range of objects is insuffecient, two records may be counted as one size in order to more accurately survey range quantity, deal with in quantity calculation
from backend.models import Area, Piece, Arearack, Userrack

def overall(user_rack):
    max_val = 0
    min_val = 0
    size_quantity = 0
    user_rack = sorted(user_rack, key=lambda user_rack: user_rack.min_size)
    reducing_rack = []
    for item in user_rack:
        reducing_rack.append(item)
    range_array = [] #{max: max min: min, range: coverage}
    done = []
    result_array = [] # check by keys to pull out, then delete; {'size': '%'%(max), 'min': min, 'max': max, 'quantity': quantity, 'extra_ids':[-associated id's, can add to quantity-]}, {'extras':[All extra id's]} don't ned to add to both, just check if current size needs them first then assign all remaining gray area id's to the next 'size'
    for user_gear in user_rack:
        size_range = user_gear.max_size - user_gear.min_size
        overlap_minimum = size_range / 6
        overlap_equatable = (size_range * 3) / 4
        median = user_gear.max_size - (size_range / 2)
        upper_overlap = user_gear.max_size - overlap_minimum
        lower_overlap = user_gear.max_size - overlap_equatable
        size_quantity = user_gear.quantity
        while len(reducing_rack) != 0:
            compatible_max = user_gear.max_size
            next_piece = False
            versatile = []
            possible_piece = ""
            next_max = 0
            next_min = 0
            recheck = []
            if user_gear in reducing_rack:
                        reducing_rack.remove(user_gear)
            for gear in reducing_rack:
                if gear != user_gear:
                    #make sure you have the greatest ranged piece in that size
                    #get a next_max/min value
                    #add cross compatible pieces to versatile
                    #add quantity of compatible only pieces to dictionary value
                    #add dictionary entry
                    #reset values that should go back to empty
                    #save values that should update untouched standards
                    #check overall coverage and handle appropriately
                    #if range of objects is insuffecient, two records may be counted as one size in order to more accurately survey range quantity, deal with in quantity calculation
                    #if current standard has 85% compatibility with checked gear and a greater upper range, create a new compatiblity set
                    if .85 <= ((user_gear.max_size - gear.min_size) / (user_gear.max_size - user_gear.min_size)) and gear.max_size > compatible_max:
                        compatible_max = gear.max_size
                        if gear in reducing_rack:
                            reducing_rack.remove(gear)
                        size_quantity = size_quantity + gear.quantity
                        #refactor to function ^
                    #otherwise, recheck for next value   
                    else:
                        recheck.append(gear)
                    
            for item in recheck:
                #is there a next item to keep coverage continuous?
                if item.min_size >= lower_overlap and item.min_size <= upper_overlap and item.max_size > user_gear.max_size:
                    next_piece = True
                    if item.max_size > next_max:
                        if possible_piece == "":
                            possible_piece = item
                        else:
                            recheck.append(possible_piece)
                            possible_piece = item
                        next_max = item.max_size
                        next_min = item.min_size
            if possible_piece != "":
                if possible_piece in recheck:
                    recheck.remove(possible_piece)
                if possible_piece in reducing_rack:
                    reducing_rack.remove(possible_piece)

            for cam in recheck:  
                #if the range crosses into the coninuous coverage range and continues past it enough to match the next size
                #cam coverage of compatible max to it's min / total coverage                      how much upper range is in the next overlapping size
                if cam.max_size - next_min != 0:
                    if .7 <= ((compatible_max - cam.min_size) / (cam.max_size - cam.min_size)) and .7 <= ((cam.max_size - next_min) / (cam.max_size - cam.min_size)):
                        versatile.append(cam) #add it to overlapping category
                        if gear in reducing_rack:
                            reducing_rack.remove(gear) #remove it from the list, put it back later if it's the best hope to have a next piece that might keep the coverage continuous

                    #find overlap sufficient to include it in the quantity of the current size
                    #not versatile, less range, similar overlap
                    elif .7 <= ((compatible_max - cam.min_size) / (cam.max_size - cam.min_size)):
                        size_quantity = size_quantity + cam.quantity
                        if gear in reducing_rack:
                            reducing_rack.remove(gear)  #remove it from the list, put it back later if it's the best hope to have a next piece that might keep the coverage continuous
            
            recheck = []
            #put something versatile back if it has a bigger max size and might keep things continuous
            if possible_piece == "":
                if versatile != []:
                    best_bet = ""
                    for item in versatile:
                        if item.max_size > compatible_max:
                            if best_bet != "":
                                if best_bet.quantity:
                                    if best_bet.quantity == 1:
                                        if best_bet.max_size < item.max_size:
                                            versatile.append(best_bet)
                                            best_bet = item
                                            versatile.remove(item)
                                            recheck.append(item)
                                else:
                                    best_bet = item
                                    versatile.remove(item)
                                    recheck.append(item)
                            else:
                                if best_bet.max_size < item.max_size:
                                    #id value might be confusing, we'll see
                                    item.quantity = item.qunatity - 1
                                    best_bet = item
                                    best_bet.qunatity = 1
                                        

                                else:
                                    #id value might be confusing, we'll see
                                    item.quantity = item.qunatity - 1
                                    best_bet = item
                                    best_bet.qunatity = 1
                    possible_piece = best_bet
            result = {"upper": compatible_max - (compatible_max / 7.67), "lower": user_gear.min_size + (user_gear.min_size / 7.67), "quantity": size_quantity, 'versatile': versatile}
            if possible_piece == "":
                result['quantity'] = result['quantity'] + len(result['versatile'])
                result['versatile'] = []
                        #build linear coverage value

                        #check dictionary for max and min values in range
                        #given the number of items, how any are in triples, doubles or singles?
                #modifying and storing covered segments:

                final_range_max = compatible_max
                final_range_min = user_gear.min_size

                if min_val == 0:
                    min_val = final_range_min
                    max_val = final_range_max
                    range_array.append({'maximum': max_val, 'minimum': min_val})
                    if user_gear in reducing_rack:
                        reducing_rack.remove(user_gear) 

                    
                #if result breaks continuity:
                elif final_range_max > max_val:
                    max_val = final_range_max
                    range_array.append({'maximum': max_val, 'minimum': min_val})
                    if user_gear in reducing_rack:
                        reducing_rack.remove(user_gear)
                    min_val = 0
                else:
                    range_array.append({'maximum': max_val, 'minimum': min_val})
                    if user_gear in reducing_rack:
                        reducing_rack.remove(user_gear) 

                reducing_rack.clear()
            else:
                if min_val == 0:
                    min_val = user_gear.min_size

                if user_gear.min_size < min_val:
                    min_val = user_gear.min_size

                if user_gear in reducing_rack:
                    reducing_rack.remove(user_gear)
                reducing_rack.clear()
            result_array.append(result)
        done.append(user_gear)
        for item in user_rack:
            if item not in done:
                reducing_rack.append(item)
    return(result_array)
         #if range of objects is insuffecient, two records may be counted as one size in order to more accurately survey range quantity, deal with in quantity calculation... maybe
def coverage(user):
    cover = Userrack.objects.filter(user=user)
    coverage_list = []
    for item in cover:
        numbered_piece = item.piece
        if item.piece.SLCD == True:
            setattr(numbered_piece, 'quantity', item.quantity)
            coverage_list.append(numbered_piece)
    
    x = overall(coverage_list)
    return x