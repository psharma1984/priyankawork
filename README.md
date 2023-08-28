# My Contribution at wildepod.org (Felidae Conservation Fund)
annotation.py : I developed a custom feature (CustomAnnotationView -- line 152) that allowed volunteers to select specific camera sites for image annotations. This allowed the volunteers to choose images for a particular camera site. The megadetector creates a bounding box around the objects in image which is then labelled by the volunteers. To provide the volunteer with a specific image from a particular website only these images are moved to the cloud buckets.
custom_fields.py : I also wrote the function get_filter_params() which was later used in (annotation.py -- AnnotateSpeciesView(line 199) and AnnotateActivityView (line 348)), to filter out images based on the criteria.
forms.py : Wrote the form class (class AnnotationForm(forms.Form) -- line 135) to render the form for "custom_annotation.html" file.
custom_annotation.html : HTML file for Custom Annotation Feature
set_priority.py : I was also involved in designing and implementing backend services that facilitated image prioritization for annotation. This helped to label certain camera sites as high priority and some as low priority for fetching the images. The form class for the HTML page is (class SetPriorityForm(forms.Form)--line 18). The view which sets priority is (Priority View - Line 63). Once the priority is selected, the user is sent to a confirm page to make sure that the selection is right (class ConfirmUpdateView -- line 112)
set_priority.html : HTML file for Set Priority feature.
set_priority_confirm.html : HTML file related to (ConfirmUpdateView (line 112 in set_priority.py))
objects.html : <script> to enable selection of only checkbox and not the label next to it, as it was sometimes being getting selected by mistake. (line 168-173)
