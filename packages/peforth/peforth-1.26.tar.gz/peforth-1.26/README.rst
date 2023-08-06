peforth
#######

A programmable python debugger allows you to abruptly setup procedures to investigate your program code on the fly at a breakpoint.
********************************************************************************************************************************************

You guys know how to bebug already. We all do.
But when it comes to Machine Learning and Tensorflow or the likes, 
things are getting annoying. A programmable debugger is what in my mind and probably in yours too. One breakpoint to investigate about everything! At this point, you can
then test whatever you want, supported by all the power of FORTH.

Debug commands in FORTH syntax
##############################

So now we need to choose an interactive UI and its syntax that 
is light weight, reliable and flexible so we won't regret of choosing it 
someday, has been there for decades so many people don't need to learn about 
another new language although we are only to use some debug commands, yet easy 
enough for new users, that's FORTH. 

Install peforth
###############

::

    pip install peforth 

For Jupyter Notebook users, we can use FORTH language to investigate python objects through peforth magics `%f` and `%%f`. For tutorials, please find and read jupyter notebooks in the 'notebook' directory of this project on GitHub.


Run peforth:
#############

Print "Hello World!"

::

    Microsoft Windows [Version 10.0.15063]
    (c) 2017 Microsoft Corporation. All rights reserved.

    c:\Users\your-working-folder>python -m peforth .' Hello World!!' cr bye
    Hello World!!

    c:\Users\your-working-folder>

    
so your peforth is working fine. 
To your application, ``import peforth`` as usual to bring in the debugger:

::

    c:\Users\your-working-folder>python
    Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import peforth
    p e f o r t h    v1.07
    source code http://github.com/hcchengithub/peforth
    Type 'peforth.ok()' to enter forth interpreter, 'exit' to come back.

    >>>


The greeing message tells us how to enter the FORTH interpreter for your 
debugging or investigating and how to come back to continue running your 
code.     
    
Let's try to debug a program
############################

::
    
    # 100.py
    
    sum = 0
    for i in range(100):
        sum += i
    print("The sum of 1..100 is ", sum)

    
Run it:

::

    c:\Users\your-working-folder>python 100.py
    The sum of 1..100 is 4950

    c:\Users\your-working-folder>

The result should be 5050 but it's not! Let's drop a breakpoint 
to see what's wrong:

::

    # 100.py with breakpoing   .----- Specify an unique command prompt to indicate where 
                               |      the breakpoint is from if there are many of them
    import peforth             |            .----- pass locals() at the breakpoint
    sum = 0                    |            |      to our debugger
    for i in range(100):       |            |               .------- use a FORTH constant   
        sum += i               |            |               |        to represent the locals()
    peforth.ok('my first breakpoint> ',loc=locals(),cmd="constant locals-after-the-for-loop")
    print("The sum of 1..100 is ", sum)


Run again:

::
    
    c:\Users\your-working-folder>python 100.py
    p e f o r t h    v1.07
    source code http://github.com/hcchengithub/peforth
    Type 'peforth.ok()' to enter forth interpreter, 'exit' to come back.

                         .--------------- at the breakpoint, type in 'words' 
                         |                command to see what have we got   
    my first breakpoint> words        .-------- It's a long list of 'words'
    ... snip .......                  |         or available commands. Don't worry, we'll use only some of them.
    expected_rstack expected_stack test-result [all-pass] *** all-pass [r r] [d d] [p 
    p] WshShell inport OK dir keys --- locals-after-the-for-loop
                                           |
                The last one is what ------' 
                we have just created throuth the breakpoint statement    
                , named "locals-after-the-for-loop"

Let's see it:

::

           print a carriage return at the end -------.
                              print the thing -----. | 
                                                   | |
    my first breakpoint> locals-after-the-for-loop . cr
    ({'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': 
    <_frozen_importlib_external.SourceFileLoader object at 0x000001DD2D737710>, 
    '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' 
    (built-in)>, '__file__': '100.py', '__cached__': None, 'peforth': <module 'peforth' 
    from 'C:\\Users\\hcche\\AppData\\Local\\Programs\\Python\\Python36\\lib\\site-packages\\pe
    forth\\__init__.py'>, 'sum': 4950, 'i': 99}, {}, 'my first breakpoint> ')
    my first breakpoint>    |           |                   |
                            |           |                   '--- our command
               our sum -----'           |                        prompt
                                        |                  indicates where the 
            99 instead of 100 ----------'                  breakpoint is from
            this is the problem !!            


Now leave the breakpoint and let the program continue:

::

    my first breakpoint> exit
    my first breakpoint> The sum of 1..100 is  4950

    c:\Users\your-working-folder>


Investigate by doing experiments right at a breakpoint
######################################################
    
When at a breakpoint in Tensorfow tutorials, I always want to
make some experiments on those frustrating *tf.something(tf.something(...),...)*
things to have a clearer understanding of them 
without leaving the underlying tutorial. Let's use the above example
again in another way to demonstrate how to do that with peforth:  

Run peforth:

::

    Microsoft Windows [Version 10.0.15063]
    (c) 2017 Microsoft Corporation. All rights reserved.

    c:\Users\your-working-folder>python
    Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import peforth
    p e f o r t h    v1.07
    source code http://github.com/hcchengithub/peforth
    Type 'peforth.ok()' to enter forth interpreter, 'exit' to come back.

    >>> peforth.ok()

    OK   <-------- Default FORTH command prompt
    OK    

Assume we are at a breakpoint and we need a procedure to
add 1..100 to get the sum of them. We are not sure if the procedure
is correct so we need to try. Now copy the procedure from 
your text editor. The ``` <py>...</py> ``` tells the debugger that 
the code within is a block of in-line python. 
The ```outport()``` function outports the given ```locals()``` to the
FORTH environment outside the in-line python block.

::

    <py>
    sum = 0
    for i in range(100):
        sum += i
    print("The sum of 1..100 is ", sum)
    outport(locals())
    </py>
    
It's a block of multiple-line text strings so we press Ctrl-D
to start a multiple-line input, copy-paste, and press another Ctrl-D
to end the multiple-line block. Like this:

::

    OK
    OK ^D
        <py>
        sum = 0
        for i in range(100):
            sum += i
        print("The sum of 1..100 is ", sum)
        outport(locals())
        </py>
    ^D
    The sum of 1..100 is  4950
    OK

Now use the 'words' command to see what have we got:

::

    OK words
    code end-code \ // <selftest> </selftest> bye /// immediate stop compyle 
    trim indent -indent <py> </py> </pyV> words . cr help interpret-only 
    compile-only literal reveal privacy (create) : ; ( BL CR word ' , 
    [compile] py: py> py:~ py>~ 0branch here! here swap ! @ ? >r r> r@ drop 
    dup over 0< + * - / 1+ 2+ 1- 2- compile if then compiling char last 
    version execute cls private nonprivate (space) exit ret rescan-word-hash 
    (') branch bool and or not (forget) AND OR NOT XOR true false "" [] {} 
    none >> << 0= 0> 0<> 0<= 0>= = == > < != >= <= abs max min doVar doNext 
    depth pick roll space [ ] colon-word create (marker) marker next abort 
    alias <> public nip rot -rot 2drop 2dup invert negate within ['] allot 
    for begin until again ahead never repeat aft else while ?stop ?dup 
    variable +! chars spaces .( ." .' s" s' s` does> count accept accept2 
    <accept> nop </accept> refill [else] [if] [then] (::) (:>) :: :> ::~ 
    :>~ "msg"abort abort" "msg"?abort ?abort" '<text> (<text>) <text> </text> 
    <comment> </comment> (constant) constant value to tib. >t t@ t> [begin] 
    [again] [until] [for] [next] modules int float drops dropall char>ASCII 
    ASCII>char ASCII .s (*debug*) *debug* readTextFile writeTextFile 
    tib.insert sinclude include type obj>keys obj2dict stringify toString 
    .literal .function (dump) dump dump2ret d (see) .members .source see dos 
    cd slice description expected_rstack expected_stack test-result 
    [all-pass] *** all-pass [r r] [d d] [p p] WshShell inport OK dir keys 
    --- i sum
    OK

Around the end of the long list after the ``` --- ``` marker we found ``` i ``` and 
``` sum ```. They are all locals() at the point in the in-line python block.
Let's see them:

::

    OK i . cr
    99
    OK sum . cr
    4950
    OK
    
Again, we found the root cause of why the sum is not 5050 because
``` i ``` didn't reach to 100 as anticipated. That's exactly how the 
python ```range()``` works and that has actually confused me many times.


Visit this project's 
`Wiki`_
pages
for more examples about how to view MNIST handwritten digit images
at the half way of your investigating in a Tensorflow tutorial, for
example, and the usages of this programmable debugger.

Have fun!
*********

- H.C. Chen, FigTaiwan, 2019.5.22
- hcchen5600@gmail.com
- Just undo it! 

Edited by: `rst online editor`_

.. _Wiki: https://github.com/hcchengithub/peforth/wiki
.. _rst online editor: http://rst.ninjs.org
.. _Jupyter Notebook: http://nbviewer.jupyter.org/
.. _Linux Users: http://robl.co/brainfuck-ipython/

