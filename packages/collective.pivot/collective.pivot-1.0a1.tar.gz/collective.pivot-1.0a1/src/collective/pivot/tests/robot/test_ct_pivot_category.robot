# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.pivot -t test_pivot_category.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.pivot.testing.COLLECTIVE_PIVOT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/collective/pivot/tests/robot/test_pivot_category.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a pivot_category
  Given a logged-in site administrator
    and an add pivot_category form
   When I type 'My pivot_category' into the title field
    and I submit the form
   Then a pivot_category with the title 'My pivot_category' has been created

Scenario: As a site administrator I can view a pivot_category
  Given a logged-in site administrator
    and a pivot_category 'My pivot_category'
   When I go to the pivot_category view
   Then I can see the pivot_category title 'My pivot_category'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add pivot_category form
  Go To  ${PLONE_URL}/++add++pivot_category

a pivot_category 'My pivot_category'
  Create content  type=pivot_category  id=my-pivot_category  title=My pivot_category

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the pivot_category view
  Go To  ${PLONE_URL}/my-pivot_category
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a pivot_category with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the pivot_category title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
