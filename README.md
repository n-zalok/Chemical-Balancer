# Chemical Balancer
## Video Demo : <https://www.youtube.com/watch?v=hl1bOQ4SydQ>
## Description:

- ### Overview
  - #### `l = list` `d = dict` `f = factor` `m = member` `r = reactant` `p = product` `e = element` `hs = hand side`
  - #### It takes input as `A + B + ... = C + D + ...` and outputs a balanced equation as `aA + bB + ... = cC + dD + ...` with the correct factors
  - #### The requirements for specific form of input are not because the intolerance of handling user's typographic mistakes but because the program needs to collect specific information
  - #### Making the input case sensitive to avoid confusion for example if the program accepted case insensitive input the program cannot differentiate between (Co = cobalt) and (CO = carbon monoxide)
  - #### Preventing the user from entering any factors is to prevent him to mislead the program resulting in wrong results
  - #### Trueness of the equation entered relies on the user for example if he\she entered `Na2Cl` which is a wrong formula for sodium chloride the program is not designed to correct it to `NaCl`
  - #### `ATOMS = e1|e2|e3|...` for all elements to be used in regex
  - #### I have tested as many equations as I could and tried many corner cases but I am not 100% sure that my program is applicable for all equations

- ### Main
  - #### The program starts with printing the instruction previously discussed in Overview
  - #### The program prompts the user for the `equation` then removes all white spaces
  - #### `invalid_input` checks if the user has typed any factors if he\she did it raises a `ValueError` which is caught by main, and the user is re prompted
  - #### The `equation` is splitted to `reactants` and `products`
  - #### `reactants` and `products` pass through `get_side()` which collects information and returns a list of dictionaries for count of each element in the member for each member for example `get_side('2Na+Cl') = [{Na: 2}, {Cl: 1}]`
  - #### The result of `get_side()` then enters `balance()` which returns a dict of {factor: member} for each member with a modified factor so it gets the correct factor for each member in the equation whose factor will be changed from 1
  - #### The result of `balance()` then enters `factorize()` which modifies all factors to be integers if they were fractions and divide the factors by the greatest common divisor to make them in the simplest form
  - #### The result of `factorize()` then enters `generate_side()` which generates the new equation with factors added
  - #### main then prints the new equation

- ### expand_side()
  - #### It reforms the input to remove each number and add the equivalent of the element with it for example `expand_side(Fe2(SO4)3) = 'FeFeSSSOOOOOOOOOOOO'
  - #### It first checks for elements inside a parenthesis using `re.findall`
  - #### Then it checks for elements outside parenthesis using `re.findall`
  - #### Then it removes all digits and parenthesis from the string

- ### get_side()
  - #### It gets the output of `expand_side` then uses `re.findall` to find all elements in the string and adds them to a dict `{element: 1}` if it is not the first time it increases the value of the element in the dict by one
  - #### It repeats this process for each member in the side(reactants or products) and adds all the dictionaries to one list `l_d_m`

- ### total()
  - #### It takes the result of `get_side()` and adds up all values in one dict which contains {element: total number of it on that side}

- ### repeat()
  - #### It takes the result of `get_side` and creates a dict of {element: times of showing up in eathier sides} and the dict is sorted by values ascending
  - #### This is useful because when you are balancing equation it is useful to start with the least repeated element because it could be balanced faster (the program will look for its count in fewer members because it doesn't show up frequently)

- ### balance():
  - #### It takes the results of both `total()` and `repeat()`
  - #### `total()` tells it if there is more of an element on the reactants side or products side
  - #### `repeat()` tells it from which element should it start to balance
  - #### It creates two dicts `d_r_f` and `d_p_f` both of which will contain {factor: member} basically it tells us what the factor is each member is multiplied by
  - #### Forever it will try to modify factors until `total(reactants) = total(products)`
  - #### For each element if it is smaller on the reactants side `number(element)` will adjust one of the factors of a member in the reactant side to make the element equal on both sides and vice versa for the products side
  - #### if the element is equal on both sides, it breaks the loop, then goes on to balance the next element
  - #### After it is done balancing each element it checks if `total(reactants) = total(products)` because balancing one element may mess up the already balanced ones if the condition isn't met it goes on to balance them again
  - #### In some conditions the program will take a wrong approach and choose wrong members to use in balancing which causes an infinite loop where all factors just keep growing to catch that `all = total_rhs|total_phs` if any value in `all.values()` is greater than 1000 it restarts `balance()` and reverses the order of members in rhs and phs
  - #### If infinite looping occured again that means the user has inputted an invalid formula so he\she is prompted again
  ```python
          errors = 0
        all = total_rhs|total_phs
        for value in all.values():
                if value > 1000:
                    rhs = sorted(r_spare, key=len, reverse=True)
                    phs = sorted(p_spare, key=len, reverse=True)
                    total_rhs = total(rhs)
                    total_phs = total(phs)
                    d_r_f = {}
                    d_p_f = {}
                    errors = errors + 1
                    break
        if errors == 2:
            raise ValueError
    ```
  - #### When the condition is met it breaks out of the bigger loop then returns two dicts `d_r_f` and `d_p_f`

- ### numbers()
  - #### It takes the smaller side of an element and searches for a member which contains this element then multiplies its factor to be equal to the other side
  - #### Then it modifies the number of each element on that side and returns a dict of {factor: member} and a new side with number of elements modified according to the factor
 ```python
  elif factor in d_m_f.keys() and m not in d_m_f.values():
      factor = factor + .001
      d_m_f[factor] = m
  ```
  - #### because if the factor is already in `d_m_f` resembling another member it will overwrite it so the small addition of .001 is to create a new {key: value} pair and the factor could be rounded later
   ```Python
   else:
      new_factor = list(d_m_f.keys())[list(d_m_f.values()).index(m)] * factor
      d_m_f.update({new_factor: m})
      del d_m_f[list(d_m_f.keys())[list(d_m_f.values()).index(m)]]
  ```
  - #### if the member's factor is already modified and it will be modified again this will remodify it and delete the old copy

- ### convert_back()
  - #### It takes `d_m_f` which will equal `{factor: {element: (number * factor)}}` (inner dict represents the member whose factor has been modified)
  - #### It divides (number * factor) by factor to retain the original member with its factor

- ### factorize()
  - #### It takes the result of `balance()`
  - #### If any factor is not an integer it multiplies all factors by the number that makes that fractional factor an integers
  - #### If all factors are divisile by a prime number it divides all factors by that number
  - #### `factors_of_unity` list contains all the numbers that have been used to get rid of fractional factors and numbers used to divide all factors by their common divisor (this factors list is used for members with factor 1 which wasn't given a factor by `balance()`)
 ```Python
 if len(keys) < len(rhs + phs):
        keys.append(1)
  ```
  - #### this is used to add factor 1 if it is in the equation by checking if the factors `len(keys)` is less than total members `len(rhs + phs)` this means there are members with the factor of one
  - #### factors in `factors_of_unity` are then multiplied to get one factor `factor_of_unity`
  - #### the function returns `r(reactants after modifying the factors), p(products after modifying factors), factor_of_unity`

- ### generate_side()
  - #### takes `(new factors generated by factorize(), members of the side, factor_of_unity)`
  - #### checks if the `member` is in `new.values` which means its factor has been modified, if it was it adds it alongside its factor to `new_side`
  - #### if it was not, it adds it alongside `factor_of_unity` to `new_side`
  - #### finally new sides are generated and returned to `main` which put them together and prints the new equation

