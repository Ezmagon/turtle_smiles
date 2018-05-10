#MIT License
#
#Copyright (c) 2018 Matthijs Jonathan Tadema
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

"""
Library containing functions to draw molecules from graphs
"""


import turtle, networkx
import turtle_smiles.structure as structure

def init():
    global window
    window = turtle.Screen()

def draw_element(t, element):
    """
    Parameters:
        t, turtle object
        element, str representing an element
    Function:
        Draws a colored dot if the element is something other than C
    """
    dot_size = 15
    element_dict = {
            "N": "blue",
            "O": "red",
            "S": "yellow"
            }
    if element in element_dict:
        t.dot(dot_size, element_dict[element])

def draw_branches(t, g, n, turn, l, angle, cyclic = False):
    """
    Parameters:
        t,      a turtle object
        g,      a molecule graph
        n,      an integer representing a node
        turn,   turn variable
        l,      bond length
        angle,  bond angle
        cyclic, determines if branch is cyclic

    Function:
        Is invoked by draw.molecule(), extracts branched subgraphs
        Passes them back to draw.molecule() to draw them
        Performs most of the logical abracadabra in determining 
        where bonds/branches should go

    No return value but recurses back into draw.molecule() to branches
    """

    # Define a bunch of variables
    old_heading = t.heading()
    t_pos = t.pos()
    new_heading = None

    # Get each branch as a separate graph
    branches = structure.extract_branches(g, n)
    for branch in branches:
        try:
            if type(branch) != networkx.classes.graph.Graph:
                # For debugging but this shouldn't fail anymore
                raise TypeError("getting branch subgraph failed type = {}".format(type(branch)))
        except TypeError as e:
            print(g, n, branch)
            raise e

        # Check if the first edge of the branch is part of a cycle
        branch_bb = structure.backbone(branch)
        first_e = list(branch_bb.edges())[0]
        a, b = first_e
        try:
            cyclic_branch = branch[a][b]["cyclic"]
        except KeyError:
            cyclic_branch = False
        
        # Spawn another turtle at this point in the opposite direction  
        if not cyclic_branch:
            new_heading = old_heading + (2 * angle * turn)
            if cyclic:
                # if the previous edge was cyclic, move out of the cycle
                new_heading += (2 * angle * turn)
        else:
            # If a cyclic branch is started, the heading should stay the same as before
            new_heading = old_heading
            # This is needed for tyrosine
            # Tyrosine doesn't work anymore anyway but i don't want to break
            # anything else
            if cyclic:
                t.right(2 * angle * turn)
            else:
                new_heading = old_heading + (2 * angle * turn)

        # For when there are two branches at a point
        # This can happen depending on how the graph was defined
        old_heading -= (2* angle * turn)
        # Draw a new "molecule" using the specified parameters
        # Use the new branch graph as the main graph
        molecule(branch, t.pos(), new_heading, turn)

def molecule(g, pos = (0, 0), rot = 30, turn = -1):
    """
    Parameters:
        g, a graph representing a molecule
        pos, a tuple representing turtle coordinates
        rot, a number representing the current turtle heading (int or float)
        turn, 1 or -1, alternates to create linear pieces of molecule
    
    Function:
        Main function for drawing the molecules
        will draw linear segments until it finds a branchpoint
        then it calls draw_branches() to extract the correct branched graph
        after which draw_branches() calls draw.molecule again

    No return value, but will call itself to draw new branches at branch points if
    it finds any
    """
    l = 80 # bond length
    angle = 60 # angle
    params = (l, angle) # to pass later to draw_branches
    # get backbone
    bb = structure.backbone(g)
    # draw backbone
    # init turtle
    t = turtle.Turtle()
    t.speed(3)
    pen_size = 1
    t.pensize(pen_size)
    # Move to starting position
    t.up()
    t.goto(pos)
    t.seth(rot)
    t.down()
    # Start drawing
    # Do stuff for the first node because otherwise it's left out of the loop
    if list(g.nodes())[0] == 0:
        # draw element for first node because it's skipped otherwise
        element = g.nodes.data("element")[0]
        draw_element(t, element)

        if g.degree(0) == 2: # For the first one, if degree is >2 there is a branch
            draw_branches(t, g, 0, turn, *params)
    for e in bb.edges():
        # Check if cyclic
        try:
            cyclic = g[e[0]][e[1]]["cyclic"]
        except KeyError:
            # If keyerror is raised, edge is not cyclic
            cyclic = False
        # Set pen thickness for single or double bond
        order = g[e[0]][e[1]]["order"]
        t.pensize(pen_size + 3 * order)
        # move forward one bond length
        t.forward(l)
        # Hide the turtle
        t.ht()
        # Reset the pensize
        t.pensize(pen_size)
        # Turn left for the next bond
        t.left(angle * turn)
        # Reverse the turning variable if not cyclic
        # if not reversed, will continue in a cycle
        if not cyclic:
            # reverse turn
            turn *= -1
        # Get the current node which is usually the highest but not always
        # This should be more robust
        n = max(e) # current node
        # Draw a colored circle for N, O, or S
        element = g.nodes.data("element")[n]
        draw_element(t, element)

        # if branchpoint
        if g.degree(n) == 3:
            # Draw a branch
            # If the branch contains more branches this will recurse
            draw_branches(t, g, n, turn, *params, cyclic = cyclic)
        # Cannot handle 4 way branches yet
        elif g.degree(n) > 3:
            raise ValueError("Cannot deal with these yet")

def done():
    window.mainloop()
