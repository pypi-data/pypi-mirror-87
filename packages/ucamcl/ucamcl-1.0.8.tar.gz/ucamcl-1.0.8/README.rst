ucamcl
======

This package provides a simple tool for checking answers
to exercises in a Jupyter notebook.

Usage::

  # Install the grader
  !pip install ucamcl

  # Log in to the grader. It will prompt you with a "log in" button.
  GRADER = ucamcl.autograder('https://markmy.solutions', course='scicomp').subsection('notes1')

  # Fetch a question. It will tell you what to do, with what parameters.
  q = GRADER.fetch_question('ex5')
  print(q)

  # Prepare your answer and submit it.
  myans = {'x': [i**2 for i in range(q['n'])]
  is_correct, answer = GRADER.submit_answer(q, myans)

This package is what the student installs in their Jupyter notebook.
The other half is a server that should be set up by the course instructor.
Contact Damon Wischik <djw1005@cam.ac.uk> for details.


