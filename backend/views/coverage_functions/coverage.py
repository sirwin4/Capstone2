#if range of objects is insuffecient, two records may be counted as one size in order to more accurately survey range quantity, deal with in quantity calculation
def coverage(user_rack):
    max_val = 0
    min_val = 0
    user_rack = sorted(user_rack, key=lambda user_rack: user_rack.min_size, reverse=True)
    reducing_rack = user_rack
    range_array = [] #{max: max min: min, range: coverage}
    second_check = []
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
            compatible_min = upper_overlap
            compatible_max = user_gear.max_size
            next_piece = False
            versatile = []
            possible_piece = ""
            next_max = 0
            next_min = 0
            recheck = []
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
                    if .85 <= ((user_gear.max_size - gear.min_size) / (user_gear.max_size - user_gear.min_size)) and gear.max_size > compatible_max and gear.min_size < (median + overlap_minimum):
                        compatible_max = gear.max_size
                        compatible_min = gear.max_size - ((gear.max_size - gear.min_size) / 6)
                        reducing_rack.remove(gear)
                        size_quantity = size_quantity + gear.quantity
                        #refactor to function ^
                    #otherwise, recheck for next value   
                    else:
                        recheck.append(gear)
                else: #take the current item out, it's getting handled
                    reducing_rack.remove(gear)
            
            for item in recheck:
                #is there a next item to keep coverage continuous?
                if item.min_size in range(lower_overlap, upper_overlap) and item.max_size > (user_gear.max_size + overlap_minimum):
                    next_piece = True
                    if item.max_size > next_max:
                        recheck.remove(item)
                        if possible_piece == "":
                            possible_piece = item
                        else:
                            recheck.append(possible_piece)
                            possible_piece = item
                        next_max = item.max_size
                        next_min = item.min_size

            for cam in recheck:  
                #if the range crosses into the coninuous coverage range and continues past it enough to match the next size
                #cam coverage of compatible max to it's min / total coverage                      how much upper range is in the next overlapping size
                if .7 <= ((compatible_max - cam.min_size) / (cam.max_size - cam.min_size)) and .7 <= ((cam.max_size - next_min) / (cam.max_size - cam.min_size)):
                    versatile.append(cam) #add it to overlapping category
                    reducing_rack.remove(cam) #remove it from the list, put it back later if it's the best hope to have a next piece that might keep the coverage continuous
                    recheck.remove(cam)

                 #find overlap sufficient to include it in the quantity of the current size
                 #not versatile, less range, similar overlap
                elif .7 <= ((compatible_max - cam.min_size) / (cam.max_size - cam.min_size)):
                    size_quantity = size_quantity + cam.quantity
                    reducing_rack.remove(cam) #remove it from the list, put it back later if it's the best hope to have a next piece that might keep the coverage continuous
                    recheck.remove(cam)
            #put something versatile back if it has a bigger max size and might keep things continuous
            if next_piece == False:
                if len(versatile):
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
                                if best_bet != "":
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
            
            if possible_piece == "":
                        #build linear coverage value

                        #check dictionary for max and min values in range
                        #given the number of items, how any are in triples, doubles or singles?
                #modifying and storing covered segments:
                final_range_max = compatible_max
                final_range_min = compatible_min
                if min_val == 0:
                    min_val = final_range_min
                    max_val = final_range_max
                #if range extends continuity:
                elif final_range_max > max_val and final_range_min <= max_val:
                    max_val = final_range_max
                #if result breaks continuity:
                elif final_range_max > max_val and final_range_min > max_val:
                    range_array.append({'maximum': max_val, 'minimum': min_val, 'range': (max_val - min_val)})
                    min_val = final_range_min
                    max_val = final_range_max
         #if range of objects is insuffecient, two records may be counted as one size in order to more accurately survey range quantity, deal with in quantity calculation... maybe