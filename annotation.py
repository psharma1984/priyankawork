import datetime
import json
import logging

import numpy as np
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Exists, OuterRef, Q
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.base import TemplateView, View
from images.forms import AnnotationForm
from images.models import (
    Activity,
    ActivityType,
    Annotator,
    BoundingBox,
    Category,
    Image,
    Species,
    SpeciesName,
    get_object_annotation_images,
)
from images.models.custom_fields import get_filter_params
from images.processors import process_activity_annotations, process_md_annotations, process_species_annotations
from locations.models import CameraStation, MacroSite, MicroSite

MAX_VOTES_PER_IMAGE = 2
CATEGORY_ANIMAL = "animal"
CATEGORY_HUMAN = "human"

class CustomAnnotationView(LoginRequiredMixin, FormView, TemplateView):
    login_url = settings.LOGIN_URL
    template_name = "images/annotate/custom_annotation.html"
    form_class = AnnotationForm

    def post(self, request, *args, **kwargs):
        form = AnnotationForm(request.POST)

        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            macrosites = form.cleaned_data["macrosites"]
            macrosite_name = macrosites.name
            camera_stations = form.cleaned_data["camera_stations"]
            annotation_choices = form.cleaned_data["annotation_choices"]
            if camera_stations:
                camera_id = camera_stations.station_id
            else:
                camera_id = "None"

            if annotation_choices == "species":
                url = (
                    reverse("images:annotate_species")
                    + f"?start_date={start_date}&end_date={end_date}&macrosite_name={macrosite_name}&camera_id={camera_id}"
                )
            elif annotation_choices == "human" or annotation_choices == "animal":
                url = reverse("images:annotate_activity", kwargs={"category": annotation_choices})
                url += f"?start_date={start_date}&end_date={end_date}&macrosite_name={macrosite_name}&camera_id={camera_id}"
            else:
                url = (
                    reverse("images:annotate_objects")
                    + f"?start_date={start_date}&end_date={end_date}&macrosite_name={macrosite_name}&camera_id={camera_id}"
                )
            return redirect(url)


# TODO: Clean up this code
class AnnotateSpeciesView(LoginRequiredMixin, TemplateView):
    login_url = settings.LOGIN_URL
    template_name = "images/annotate/species.html"

    def get(self, request, *args, **kwargs):
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        camera_id = None if self.request.GET.get("camera_id") == "None" else self.request.GET.get("camera_id")
        macrosite_name = self.request.GET.get("macrosite_name")

        self.filterset = get_filter_params(start_date, end_date, macrosite_name, camera_id)

        return super().get(request, *args, **kwargs)
######### more code
##################
###################
    
# TODO: Clean up this code
class AnnotateActivityView(LoginRequiredMixin, TemplateView):
    login_url = settings.LOGIN_URL
    template_name = "images/annotate/activity.html"

    def get(self, request, *args, **kwargs):
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        camera_id = None if self.request.GET.get("camera_id") == "None" else self.request.GET.get("camera_id")
        macrosite_name = self.request.GET.get("macrosite_name")
        self.filterset = get_filter_params(start_date, end_date, macrosite_name, camera_id)

        return super().get(request, *args, **kwargs)
######### more code
##################
###################
   
