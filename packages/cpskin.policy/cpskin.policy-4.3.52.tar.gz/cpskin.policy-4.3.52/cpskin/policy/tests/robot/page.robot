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

Modèle de document
    Go to  ${PLONE_URL}/ma-commune/vie-politique/college-communal/le-college-communal/edit
    Wait until element is visible  cke_17  10
    Highlight  cke_17  3  solid
    Capture and crop page screenshot  doc/4-1 bouton-modèles.png  id=formfield-form-widgets-IRichText-text
    Clear highlight  cke_17
    Click Element  cke_17
    Wait until element is visible  cke_94_uiElement  10
    Click Element  css=#cke_94_uiElement a:first-child
    Sleep  5
    Capture and crop page screenshot  doc/4-1 inserer-modèles.png  id=portal-columns
    Click Element  form-buttons-save
    Go to  ${PLONE_URL}/ma-commune/vie-politique/college-communal
    Click Element  plone-contentmenu-display
    Wait until element is visible  contextSetDefaultPage
    Highlight  contextSetDefaultPage  3  solid
    Capture and crop page screenshot  doc/4-1 modèle-vue-par-défaut.png  id=portal-columns
    Click Element  contextSetDefaultPage
    Click Element  css=[name="form.button.Save"]
    Clear highlight  contextSetDefaultPage

Mise en page
    Go to  ${PLONE_URL}/evenements/carnaval/edit
    Wait until element is visible  cke_56  10
    Highlight  cke_56  3  solid
    Capture and crop page screenshot  doc/4-2 bouton-images.png  id=formfield-form-widgets-IRichText-text
    Clear highlight  cke_56
    Click Element  cke_56
    Wait until element is visible  cke_102_label
    ${note1}  Add pointy note  cke_102_label  1  width=25  background=#F70909  color=#ffffff
    ${note2}  Add pointy note  css=#cke_116_uiElement .cke_dialog_ui_hbox_first  2  width=25  background=#F70909  color=#ffffff
    ${note3}  Add pointy note  cke_124_radio_input_label  3  width=25  background=#F70909  color=#ffffff
    ${note4}  Add pointy note  cke_131_uiElement  4  width=25  background=#F70909  color=#ffffff
    ${opacity}  Update element style  css=.cke_dialog_background_cover  opacity  0
    ${z-index}  Update element style  css=.cke_dialog.cke_browser_gecko.cke_ltr.cke_single_page  z-index  0
    Capture and crop page screenshot  doc/4-2 dialogue-image.png  css=.cke_dialog_background_cover
    ${z-index}  Update element style  css=.cke_dialog.cke_browser_gecko.cke_ltr.cke_single_page  z-index  10010
    Remove Element  ${note1}
    Remove Element  ${note2}
    Remove Element  ${note3}
    Remove Element  ${note4}
    Click Element  cke_144_label
    Highlight  cke_52  3  solid
    Capture and crop page screenshot  doc/4-2 bouton-lien.png  id=formfield-form-widgets-IRichText-text
    Clear highlight  cke_52
    Click Element  cke_52
    Wait until element is visible  cke_193_uiElement  10
    ${note1}  Add pointy note  css=#cke_195_uiElement #cke_193_uiElement  1  width=25  background=#F70909  color=#ffffff
    ${note2}  Add pointy note  css=#cke_195_uiElement #cke_188_textInput  2  width=25  background=#F70909  color=#ffffff
    ${z-index}  Update element style  css=.cke_dialog.cke_browser_gecko.cke_ltr  z-index  0
    Capture and crop page screenshot  doc/4-2 dialogue-lien.png  css=.cke_dialog_background_cover
    Remove Element  ${note1}
    Remove Element  ${note2}
    ${lien1}  Input text  cke_188_textInput  www.imio.be
    ${note3}  Add pointy note  css=#cke_195_uiElement #cke_188_textInput  1  width=25  background=#F70909  color=#F70909
    Highlight  cke_target_282  3  solid
    Capture and crop page screenshot  doc/4-2 lien-externe.png  css=.cke_dialog_background_cover
    Clear highlight  cke_target_282
    ${z-index}  Update element style  css=.cke_dialog.cke_browser_gecko.cke_ltr  z-index  10010
    Remove Element  ${lien1}
    Remove Element  ${note3}
    Click Element  cke_target_282
    Click Element  css=#cke_218_select [value="_blank"]
    ${z-index}  Update element style  css=.cke_dialog.cke_browser_gecko.cke_ltr  z-index  0
    ${note1}  Add pointy note  css=#cke_218_select [value="_blank"]  1  width=25  background=#F70909  color=#F70909
    Capture and crop page screenshot  doc/4-2 lien-blank.png  css=.cke_dialog_background_cover
    ${z-index}  Update element style  css=.cke_dialog.cke_browser_gecko.cke_ltr  z-index  10010
    Remove Element  ${note1}
    Click Element  cke_info_217
    Click Element  css=#cke_182_select [value="email"]
    ${lien2}  Input text  cke_206_textInput  support@imio.be
    ${z-index}  Update element style  css=.cke_dialog.cke_browser_gecko.cke_ltr  z-index  0
    ${note1}  Add pointy note  cke_182_select  1  width=25  background=#F70909  color=#ffffff
    ${note2}  Add pointy note  cke_206_textInput  2  width=25  background=#F70909  color=#ffffff
    Capture and crop page screenshot  doc/4-2 lien-mail.png  css=.cke_dialog_background_cover
    ${z-index}  Update element style  css=.cke_dialog.cke_browser_gecko.cke_ltr  z-index  10010
    Remove Element  ${lien2}
    Remove Element  ${note1}
    Remove Element  ${note2}    
    Click Element  css=#cke_182_select [value="url"]
    Click Element  cke_336_label
    Click Element  form-buttons-cancel

Style prédéfinis
    Go to  ${PLONE_URL}/evenements/carnaval/edit
    ${margin}  Update element style  cke_11  margin-right  7px
    Highlight  cke_11  3  solid
    Clear Highlight  cke_11
    Capture and crop page screenshot  doc/4-3 bouton-styles.png  id=formfield-form-widgets-IRichText-text
    Highlight  cke_32  3  solid
    Capture and crop page screenshot  doc/4-3 bouton-format.png  id=formfield-form-widgets-IRichText-text
    Click Element  form-buttons-cancel
    
Configuration collectiveGeo
    Go to  ${PLONE_URL}/@@collectivegeo-controlpanel
    Click Element  form-widgets-map_viewlet_position-2
    Input text  css= input[name="geocoding-address"]  mornimont
    Click Button  css=#geosettings-cgmap-geocoder button
    Click Element  css=#geosettings-cgmap-geocoder .results    
    ${couche}  Add pointy note  form-widgets-default_layers-to  1  width=25  background=#F70909  color=#ffffff
    ${position}  Add pointy note  form-widgets-map_viewlet_position  2  width=25  background=#F70909  color=#ffffff
    ${adresse}  Add pointy note  css= input[name="geocoding-address"]  3  width=25  background=#F70909  color=#ffffff
    ${zoom}  Add pointy note  OpenLayers_Control_Zoom_6  0  width=25  background=#F70909  color=#F70909
    ${pointer}  Add pointy note  css=#OpenLayers_Control_EditingToolbar_74 .olControlDrawFeaturePointItemInactive.olButton  0  width=25  background=#F70909  color=#F70909
    Capture and crop page screenshot  doc/4-4 configuration-collectivegeo.png  id=visual-portal-wrapper
    Click Element  form-buttons-apply
    
Ajouter un plan
    Go to  ${PLONE_URL}/evenements/concert/edit
    Highlight  fieldsetlegend-coordinates  3  solid
    Capture and crop page screenshot  doc/4-4 onglet-plan.png  id=edit-bar  css=.formTabs
    Clear highlight  fieldsetlegend-coordinates
    Click Element  fieldsetlegend-coordinates
    ${adresse}  Add pointy note  css=#form-widgets-ICoordinates-coordinates-map-geocoder button  1  width=25  background=#F70909  color=#ffffff
    ${pointer}  Add pointy note  css=#OpenLayers_Control_EditingToolbar_97 .olControlDrawFeaturePointItemInactive.olButton  3  width=25  background=#F70909  color=#ffffff
    Input text  css= input[name="geocoding-address"]  Zoning Industriel, 34 5190 Mornimont
    Click Element  css=#form-widgets-ICoordinates-coordinates-map-geocoder button
    Wait until element is visible  css=#form-widgets-ICoordinates-coordinates-map-geocoder .results  10
    Capture and crop page screenshot  doc/4-4 ajout-plan.png  id=visual-portal-wrapper



*** Keywords ***
Suite Setup
    Open test browser
    Enable autologin as  Manager
    Set Window Size  1280  800
    Set Suite Variable  ${CROP_MARGIN}  0

    
