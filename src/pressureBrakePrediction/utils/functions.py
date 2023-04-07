
def change_dtype(x):
        """This function is used to change data type of feature
           and to make NaN where it find "na".

           args:
                x: input feature
           return:
                float: cast feature into float
        """
        if x == "na":
            return float('nan')
        else:
            return float(x)
        
def target_label_encoding(y):

    """This functions helps to encode target feature into
       0 or 1 depending upon the label "neg" or "pos".

       args:
            y: target or output feature

       return:
            integer: 0 or 1 depending upon the "neg" or "pos"
    """
    if y == "neg":
        return 0
    else:
        return 1