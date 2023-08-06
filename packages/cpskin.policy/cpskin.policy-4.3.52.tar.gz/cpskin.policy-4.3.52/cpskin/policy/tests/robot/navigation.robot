*** Settings ***
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot
Resource  common.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  plone.app.robotframework.keywords.Debugging
Library  Selenium2Screenshots

Suite Setup  Suite Setup
Suite Teardown  Close all browsers

*** Test cases ***

Concept
    Go to  ${PLONE_URL}
    Page should contain  Site réalisé en collaboration
    Capture and crop page screenshot  doc/3-1 thèmes.png  id=top-search-logo  id=top-navigation
    
Créer la navigation
    Go to  ${PLONE_URL}/ma-commune/services-communaux/informatique
    Highlight  portal-breadcrumbs  3  solid
    Update element style  portal-breadcrumbs  margin-top  10px
    Capture and crop page screenshot  doc/3-3 création.png  id=top-navigation  id=portal-breadcrumbs  css=#content .documentFirstHeading
    Clear highlight  portal-breadcrumbs
    Update element style  portal-breadcrumbs  margin-top  0px
    Go to  ${PLONE_URL}/folder_contents
    Highlight  folder-contents-item-ma-commune  3  solid
    Capture and crop page screenshot  doc/3-3 content-état.png  id=listing-table
    Clear highlight  folder-contents-item-ma-commune
    Go to  ${PLONE_URL}/ma-commune/services-communaux/heures-douverture
    Click Element  plone-contentmenu-cpskin-configurations
    Highlight  plone-contentmenu-cpskin-configurations-enable_direct_access  3  solid
    Capture and crop page screenshot  doc/3-4 ajout-accès-direct.png  id=portal-columns
    Wait until element is visible  plone-contentmenu-cpskin-configurations-enable_direct_access  10
    Click Element  plone-contentmenu-cpskin-configurations-enable_direct_access

Créer la navigation je suis et je trouve
    Go to  ${PLONE_URL}
    Click Element  plone-contentmenu-factories
    Highlight  document  3  solid
    Capture and crop page screenshot  doc/3-5 ajout-doc-mot-clés.png  id=top-navigation  id=portal-columns
    Clear highlight  document
    Go to  ${PLONE_URL}/mot-cles/edit
    Highlight  fieldsetlegend-categorization  3  solid
    Capture and crop page screenshot  doc/3-5 onglet-catégorisation.png  id=portal-columns
    Clear highlight  fieldsetlegend-categorization
    Click Element  fieldsetlegend-categorization
    ${note3}  Add pointy note  css=#formfield-form-widgets-IISearchTags-isearchTags .horizontal  Mot clés Je Cherche  width=176  background=#F70909  color=#fff  position=top
    ${note4}  Add pointy note  css=#formfield-form-widgets-IIAmTags-iamTags  Mot clés Je suis  background=#F70909  color=#fff  position=top
    Capture and crop page screenshot  doc/3-5 création-catégorisation.png  id=portal-columns
    Remove Element  ${note3}
    Remove Element  ${note3}
    Click Element  form-buttons-cancel
    Go to  ${PlONE_URL}/ma-commune/services-communaux/population-etat-civil/edit
    Click Element  fieldsetlegend-categorization
    Click Element  css=#form-widgets-IIAmTags-iamTags #form-widgets-IIAmTags-iamTags-2
    Capture and crop page screenshot  doc/3-5 sélectionner-mot-clés.png  id=portal-columns
    Click Element  form-buttons-save
    Go to  ${PLONE_URL}/je-suis/nouvel-habitant
    Capture and crop page screenshot  doc/3-5 ajout-dossier-mot-clés.png  id=portal-columns
    Click Element  plone-contentmenu-actions
    Highlight  css=[id*="faceted"][id*=".enable"]  3  solid
    Clear highlight  css=[id*="faceted"][id*=".search"]
    Capture and crop page screenshot  doc/3-5 action-facette.png  id=portal-columns
    Go to  ${PLONE_URL}/je-suis/nouvel-habitant/@@faceted_subtyper/enable
    Wait until element is visible  css=[id*="configure"]
    ${note}  Add pointer  css=#content-views [id*="configure"]
    Wait until element is visible  css=.eea-preview-items  10
    Capture and crop page screenshot  doc/3-5 critère-facette.png  id=portal-columns
    Remove Element  id=${note}
    Click Element  css=#content-views [id*="configure"]
    ${note}  Add pointer  css=#c3_widget.faceted-criteria-widget .ui-icon.ui-icon-trash
    ${note1}  Add pointer  css=#c1_widget.faceted-widget.faceted-checkboxes-widget.faceted-checkbox-widget.section-portal-type.faceted-count .ui-icon.ui-icon-trash
    Click Element  css=option[value="20"]
    Click Element  css=option[value="sortable_title"]
    Click Element  css=input[value="reversed"]
    Highlight  css=.faceted-resultsperpage-widget .faceted_select  3  solid
    Highlight  css=.section-sort-on form  3  solid
    Capture and crop page screenshot  doc/3-5 création-action-facette.png  id=portal-columns
    Remove Element  id=${note}
    Remove Element  id=${note1}


*** Keywords ***
Suite Setup
    Open test browser
    Enable autologin as  Manager
    Set Window Size  1280  800
    Set Suite Variable  ${CROP_MARGIN}  0

    
