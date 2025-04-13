#program for balancing chemical reactions
import re
import math
from fractions import Fraction
import copy
from elements import elements
#list of all elements to be used in regex
atoms = sorted(elements.AllSymbols, key=lambda x: -len(x))
ATOMS = '|'.join(atoms)

# `l = list` `d = dict` `f = factor` `m = member`
# `r = reactant` `p = product` `e = element` `hs = hand side`

def main():
    while True:
        try:
            #instructions
            print("please follow these instructions\n"
                  "1.type the equation in this form:\n"
                  "  A + B + ... = C + D + ...\n"
                  "2. make sure to type chemical symbols right\n"
                  "  (Cl not cl) because (Co = cobalt) while (CO = carbon monoxide)\n"
                  "3. don't type any factors in the equation (this is the program's job to do)\n"
                  "4. the program doesn't confirm the trueness of any equation so\n"
                  "  it will balance a non existing formula if it contains same elements on each side\n"
                  "5. the program only balances chemical equations not nuclear")

            equation = input('Chemical equation: ').replace(' ', '')
            #checking if the user used factors in his equation
            invalid_input = re.findall(rf'((?:\+|=|^)(?:\d)(?:\(?)(?:{ATOMS})(?:\)?))', equation)
            if len(invalid_input) > 0:
                raise ValueError
            reactants, products = equation.split('=')
            l_d_r = get_side(reactants)
            l_d_p = get_side(products)
            d_r_f, d_p_f = balance(l_d_r, l_d_p)
            break
        except ValueError:
            pass
    r, p, factor = factorize(d_r_f, d_p_f, l_d_r, l_d_p)
    new_reactant = generate_side(r, reactants, factor)
    new_product = generate_side(p, products, factor)
    new_equation = new_reactant + new_product[:-2]
    print(new_equation)


def expand_side(side):
    #checks for every element with a number
    #then replaces the number with the string of (element * number)
    side_expanded = []
    for m in list(side.split('+')):
        m_parenthesis = re.findall(r'\((.+)\)(\d+)', m)
        for e in m_parenthesis:
            m = m.replace(e[0], '', 1) + (e[0] * int(e[1]))
        m_direct = re.findall(rf'({ATOMS}{1})(\d+)', m)
        for e in m_direct:
            m = m.replace(e[0], '', 1) + (e[0] * int(e[1]))
        side_expanded.append(m)
    side_expanded_2 = []
    for m in side_expanded:
        m = m.replace('(', '').replace(')', '')
        m = re.sub(r'[0-9]', '', m)
        side_expanded_2.append(m)

    return side_expanded_2


def get_side(side):
    #returns a list of dictionaries for count of each element in the member for each member
    side_expanded = expand_side(side)
    l_d_m = []
    for m in side_expanded:
        member = re.findall(rf'{ATOMS}', m)
        if len(list(m)) == len(list(''.join(member))):
            d_m = {}
            for e in member:
                if e not in d_m:
                    d_m[e] = 1
                elif e in d_m:
                    d_m[e] = d_m[e] + 1
            l_d_m.append(d_m)
        else:
            raise ValueError

    return sorted(l_d_m, key=len)


def total(side):
    #returns a dict of {element: the total number of it in one side}
    d_t_e = {}
    for m in side:
        for e in m:
            if e not in d_t_e:
                d_t_e[e] = m[e]
            elif e in d_t_e:
                d_t_e[e] = d_t_e[e] + m[e]

    return d_t_e


def repeat(rhs, phs):
    #returns a dict of each element and its repeatition of showing in both sides
    both_sides = rhs + phs
    reps = {}
    for m in both_sides:
        for e in m:
            if e not in reps:
                reps[e] = 1
            elif e in reps:
                reps[e] = reps[e] + 1
    reps = dict(sorted(reps.items(), key=lambda item: item[1]))

    return reps


def numbers(d_m_f, total_ghs, total_shs, side, e):
    #returns d_m_f which is a dict of {factor: member}
    #returns side which is the new number of elements after multipling by factor
    for m in side:
        if e in m.keys():
            factor = (total_ghs[e] - total_shs[e] + m[e]) / m[e]
            #modifing the original number of elements on the side
            for _ in m:
                m[_] = m[_] * factor
            #adding the {factor: member} to d_m_f
            if factor not in d_m_f.keys() and m not in d_m_f.values():
                d_m_f[factor] = m
            #if the factor is already in d_m_f it will overwrite it so
            #we increase the factor slightly to be different
            elif factor in d_m_f.keys() and m not in d_m_f.values():
                factor = factor + .001
                d_m_f[factor] = m
            #if the member was added to d_m_f before,
            #it multiplies its current factor by the new one to
            #create a new {factor: member} pair then deletes the old pair
            else:
                new_factor = list(d_m_f.keys())[list(d_m_f.values()).index(m)] * factor
                d_m_f.update({new_factor: m})
                del d_m_f[list(d_m_f.keys())[list(d_m_f.values()).index(m)]]
            break

    return d_m_f, side


def convert_back(d_m_f):
    #converts member to its original form
    for (m, factor) in zip(d_m_f.values(), d_m_f.keys()):
        for e in m:
            m[e] = int(round(m[e] / factor))
    return d_m_f


def balance(rhs, phs):
    #returns a dict of (factor: member) for each member with a modified factor
    reps = repeat(rhs, phs)
    r_og = copy.deepcopy(rhs)
    p_og = copy.deepcopy(phs)
    total_rhs = total(rhs)
    total_phs = total(phs)
    d_r_f = {}
    d_p_f = {}
    while True:
        for e in reps.keys():
            while True:
                if round(total_rhs[e], 4) > round(total_phs[e], 4):
                    new_d_p_f, new_phs = numbers(d_p_f, total_rhs, total_phs, phs, e)
                    d_p_f.update(new_d_p_f)
                    total_phs = total(new_phs)

                elif round(total_rhs[e], 4) < round(total_phs[e], 4):
                    new_d_r_f, new_rhs = numbers(d_r_f, total_phs, total_rhs, rhs, e)
                    d_r_f.update(new_d_r_f)
                    total_rhs = total(new_rhs)

                elif round(total_rhs[e], 4) == round(total_phs[e], 4):
                    break

        #checks for the completion of balance
        x = 0
        for (r_e, p_e) in zip(sorted(total_rhs), sorted(total_phs)):
            if round(total_rhs[r_e], 4) == round(total_phs[p_e], 4):
                x = x + 1
        if x == len(total_rhs):
            break

        #checks for infinite looping if the factors got too big
        #it reverses the order in which the balance is occuring
        # if factors got big again this indicates an error from the user
        errors = 0
        both_sides = total_rhs|total_phs
        for value in both_sides.values():
            if value > 1000:
                rhs = sorted(r_og, key=len, reverse=True)
                phs = sorted(p_og, key=len, reverse=True)
                total_rhs = total(rhs)
                total_phs = total(phs)
                d_r_f = {}
                d_p_f = {}
                errors = errors + 1
                break
        if errors == 2:
            raise ValueError

    return convert_back(d_r_f), convert_back(d_p_f)


def factorize(r, p, rhs, phs):
    #returns a modified (d_r_f and d_p_f)
    #returns factor(all factors multiplied) to be used for members with no factor
    factors_of_unity = []

    #getting rid of fraction factors
    keys = list(r.keys()) + list(p.keys())
    for k in keys:
        remain = k - math.floor(k)
        if .01 < remain < .99:
            remain = Fraction(remain).limit_denominator(max_denominator=10)
            factor = remain.denominator
            if factor not in factors_of_unity:
                factors_of_unity.append(factor)
                for e in list(r.keys()):
                    r[e * factor] = r.pop(e)
                for e in list(p.keys()):
                    p[e * factor] = p.pop(e)

    #factoring out the greatest common factor
    factor_of_unity = round(math.prod(factors_of_unity))
    primes = [2, 3, 5, 7]
    while True:
        y = 0
        for prime in primes:
            x = 0
            keys = list(r.keys()) + list(p.keys())
            #this 1 addition to account for members with factor of 1 in the equation
            if len(keys) < len(rhs + phs):
                keys.append(1 * factor_of_unity)
            for k in keys:
                if round(k) % prime == 0:
                    x = x + 1
            if x == len(keys):
                factors_of_unity.append(1 / prime)
                for e in list(r.keys()):
                    r[e / prime] = r.pop(e)
                for e in list(p.keys()):
                    p[e / prime] = p.pop(e)
                y = y + 1
        if y == 0:
            break

    factor_of_unity = round(math.prod(factors_of_unity))
    return r, p, factor_of_unity


def generate_side(new, members,factor_of_unity):
    #returns the new side with all factors added
    #if the member from original equation is in the dict of (factor: member)
    #it returns it alongside the factor
    #if it is not in the dict
    #it returns it alongside the factor_of_unity
    new_side = str('')
    side = members.split('+')
    for m in side:
        if get_side(m)[0] in new.values():
            factor = round(list(new.keys())[list(new.values()).index(get_side(m)[0])])
            if factor == 1:
                factor = ''
            new_side = new_side + f'{factor}{m} + '
        else:
            if factor_of_unity == 1:
                factor_of_unity = ''
            new_side = new_side + f'{factor_of_unity}{m} + '
    new_side = new_side[:-2] + '= '

    return new_side


if __name__ == '__main__':
    main()
