"""Configuration module for mapping Django models to Saleor product types."""

from dataclasses import dataclass
from typing import Any, List

from openedx.core.djangoapps.content.course_overviews.models import CourseOverview  # pylint: disable=import-error


@dataclass
class ModelToSaleorAttribute():
    """
    Maps a model attribute to a Saleor product attribute.

    Args:
        model_attribute (str): Name of the attribute in the model.
        product_attribute (str): Corresponding attribute name in Saleor.
    """
    model_attribute: str
    product_attribute: str


@dataclass
class SaleorConfig():
    """
    Base configuration for mapping a Django model to a Saleor product type.

    Args:
        model (Any): The Django model class to map.
        product_type_name (str): Name of the Saleor product type.
        attributes_mapping (List[ModelToSaleorAttribute]): List of attribute mappings.
    """
    model: Any
    product_type_name: str
    attributes_mapping: List[ModelToSaleorAttribute]


class EdxCourseOverviewSaleorConfig(SaleorConfig):
    """
    Configuration for mapping the CourseOverview model to the Saleor 'Course' product type.

    Attributes:
        model (Any): The CourseOverview model class.
        product_type_name (str): The Saleor product type name ("Course").
        attributes_mapping (List[ModelToSaleorAttribute]): Attribute mappings between CourseOverview and Saleor.
    """

    def __init__(self):
        super().__init__(
            model=CourseOverview,
            product_type_name="Course",
            attributes_mapping=[
                ModelToSaleorAttribute("id", "Course ID"),
                ModelToSaleorAttribute("banner_image_url", "Banner Image URL"),
                ModelToSaleorAttribute("course_image_url", "Course Image URL"),
                ModelToSaleorAttribute("start", "Course Start Date"),
                ModelToSaleorAttribute("end", "Course End Date"),
                ModelToSaleorAttribute("enrollment_start", "Enrollment Start Date"),
                ModelToSaleorAttribute("enrollment_end", "Enrollment End Date"),
                ModelToSaleorAttribute("self_paced", "Self Paced"),
                ModelToSaleorAttribute("eligible_for_financial_aid", "Eligible For Financial Aid"),
                ModelToSaleorAttribute("org", "Organization"),
                ModelToSaleorAttribute("language", "Language"),
            ]
        )
