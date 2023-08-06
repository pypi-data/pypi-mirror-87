from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

__NAMESPACE__ = "http://momotor.org/1.0"


@dataclass
class FileComplexType:
    """
    :ivar any_element:
    :ivar id:
    :ivar ref:
    :ivar name:
    :ivar class_value:
    :ivar src:
    :ivar type:
    :ivar encoding:
    :ivar any_attributes:
    """
    class Meta:
        name = "fileComplexType"

    any_element: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    class_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    src: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    encoding: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    any_attributes: Dict = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##any",
        }
    )


@dataclass
class LinkComplexType:
    """
    :ivar src:
    """
    class Meta:
        name = "linkComplexType"

    src: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class MetaComplexType:
    """
    :ivar name:
    :ivar version:
    :ivar author:
    :ivar description:
    :ivar source:
    :ivar generator:
    """
    class Meta:
        name = "metaComplexType"

    name: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    version: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    author: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    description: List["MetaComplexType.Description"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    source: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    generator: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )

    @dataclass
    class Description:
        """
        :ivar any_element:
        :ivar lang:
        :ivar base:
        :ivar type:
        :ivar encoding:
        :ivar other_attributes:
        """
        any_element: List[object] = field(
            default_factory=list,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
                "mixed": True,
            }
        )
        lang: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "namespace": "http://www.w3.org/XML/1998/namespace",
            }
        )
        base: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )
        type: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )
        encoding: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )
        other_attributes: Dict = field(
            default_factory=dict,
            metadata={
                "type": "Attributes",
                "namespace": "##other",
            }
        )


@dataclass
class OptionComplexType:
    """
    :ivar any_element:
    :ivar id:
    :ivar ref:
    :ivar name:
    :ivar value:
    :ivar domain:
    :ivar external:
    :ivar description:
    :ivar type:
    :ivar encoding:
    :ivar any_attributes:
    """
    class Meta:
        name = "optionComplexType"

    any_element: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    domain: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    external: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    encoding: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    any_attributes: Dict = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##any",
        }
    )


class OutcomeSimpleType(Enum):
    """
    :cvar PASS:
    :cvar FAIL:
    :cvar ERROR:
    """
    PASS = "pass"
    FAIL = "fail"
    ERROR = "error"


@dataclass
class PropertyComplexType:
    """
    :ivar any_element:
    :ivar name:
    :ivar value:
    :ivar accept:
    :ivar type:
    :ivar encoding:
    :ivar any_attributes:
    """
    class Meta:
        name = "propertyComplexType"

    any_element: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    accept: Optional["PropertyComplexType.Accept"] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    encoding: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    any_attributes: Dict = field(
        default_factory=dict,
        metadata={
            "type": "Attributes",
            "namespace": "##any",
        }
    )

    class Accept(Enum):
        """
        :cvar EQ:
        :cvar NE:
        :cvar LT:
        :cvar LE:
        :cvar GT:
        :cvar GE:
        :cvar ONE_OF:
        :cvar IN_RANGE:
        :cvar ANY:
        :cvar NONE:
        """
        EQ = "eq"
        NE = "ne"
        LT = "lt"
        LE = "le"
        GT = "gt"
        GE = "ge"
        ONE_OF = "one-of"
        IN_RANGE = "in-range"
        ANY = "any"
        NONE = "none"


@dataclass
class ResourceComplexType:
    """
    :ivar any_element:
    :ivar name:
    :ivar value:
    """
    class Meta:
        name = "resourceComplexType"

    any_element: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


class StepComplexTypePriority(Enum):
    """
    :cvar MUST_PASS:
    :cvar HIGH:
    :cvar NORMAL:
    :cvar LOW:
    :cvar DEFAULT:
    """
    MUST_PASS = "must-pass"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"
    DEFAULT = "default"


@dataclass
class FilesComplexType:
    """
    :ivar file:
    :ivar baseclass:
    :ivar basename:
    :ivar basesrc:
    """
    class Meta:
        name = "filesComplexType"

    file: List[FileComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    baseclass: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    basename: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    basesrc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class OptionsComplexType:
    """
    :ivar option:
    :ivar domain:
    """
    class Meta:
        name = "optionsComplexType"

    option: List[OptionComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    domain: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class PropertiesComplexType:
    """
    :ivar property:
    """
    class Meta:
        name = "propertiesComplexType"

    property: List[PropertyComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )


@dataclass
class ResourcesComplexType:
    """
    :ivar resource:
    """
    class Meta:
        name = "resourcesComplexType"

    resource: List[ResourceComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )


@dataclass
class CheckletComplexType:
    """
    :ivar repository:
    :ivar link:
    :ivar index:
    :ivar package_version:
    :ivar resources:
    :ivar id:
    :ivar ref:
    :ivar name:
    :ivar extras:
    :ivar version:
    :ivar entrypoint:
    """
    class Meta:
        name = "checkletComplexType"

    repository: List["CheckletComplexType.Repository"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    link: List[LinkComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    index: List[LinkComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    package_version: List["CheckletComplexType.PackageVersion"] = field(
        default_factory=list,
        metadata={
            "name": "package-version",
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    resources: List[ResourcesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    extras: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    entrypoint: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )

    @dataclass
    class Repository:
        """
        :ivar src:
        :ivar type:
        :ivar revision:
        """
        src: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
        type: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
        revision: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )

    @dataclass
    class PackageVersion:
        """
        :ivar name:
        :ivar version:
        """
        name: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
        version: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )


@dataclass
class ConfigComplexType:
    """
    :ivar meta:
    :ivar options:
    :ivar files:
    :ivar id:
    """
    class Meta:
        name = "configComplexType"

    meta: List[MetaComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    options: List[OptionsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    files: List[FilesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class DependsComplexType:
    """
    :ivar options:
    :ivar step:
    """
    class Meta:
        name = "dependsComplexType"

    options: List[OptionsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    step: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class ExpectComplexType:
    """
    :ivar properties:
    :ivar files:
    :ivar id:
    :ivar ref:
    :ivar step:
    :ivar outcome:
    """
    class Meta:
        name = "expectComplexType"

    properties: List[PropertiesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    files: List[FilesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    step: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    outcome: Optional[OutcomeSimpleType] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class ProductComplexType:
    """
    :ivar meta:
    :ivar options:
    :ivar properties:
    :ivar files:
    :ivar id:
    """
    class Meta:
        name = "productComplexType"

    meta: List[MetaComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    options: List[OptionsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    properties: List[PropertiesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    files: List[FilesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class CheckletsComplexType:
    """
    :ivar checklet:
    :ivar basename:
    """
    class Meta:
        name = "checkletsComplexType"

    checklet: List[CheckletComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    basename: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Config(ConfigComplexType):
    class Meta:
        name = "config"
        namespace = "http://momotor.org/1.0"


@dataclass
class DependenciesComplexType:
    """
    :ivar depends:
    """
    class Meta:
        name = "dependenciesComplexType"

    depends: List[DependsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )


@dataclass
class ExpectedResultComplexType:
    """
    :ivar expect:
    :ivar id:
    :ivar ref:
    """
    class Meta:
        name = "expectedResultComplexType"

    expect: List[ExpectComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Product(ProductComplexType):
    class Meta:
        name = "product"
        namespace = "http://momotor.org/1.0"


@dataclass
class ResultComplexType:
    """
    :ivar checklet:
    :ivar properties:
    :ivar options:
    :ivar files:
    :ivar step:
    :ivar outcome:
    """
    class Meta:
        name = "resultComplexType"

    checklet: List[CheckletComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    properties: List[PropertiesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    options: List[OptionsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    files: List[FilesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    step: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    outcome: Optional[OutcomeSimpleType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class Result(ResultComplexType):
    class Meta:
        name = "result"
        namespace = "http://momotor.org/1.0"


@dataclass
class ResultsComplexType:
    """
    :ivar meta:
    :ivar checklets:
    :ivar result:
    :ivar id:
    """
    class Meta:
        name = "resultsComplexType"

    meta: List[MetaComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    checklets: List[CheckletsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    result: List[ResultComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class StepComplexType:
    """
    :ivar meta:
    :ivar dependencies:
    :ivar checklet:
    :ivar resources:
    :ivar options:
    :ivar files:
    :ivar id:
    :ivar ref:
    :ivar priority:
    """
    class Meta:
        name = "stepComplexType"

    meta: List[MetaComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    dependencies: List[DependenciesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    checklet: List[CheckletComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    resources: List[ResourcesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    options: List[OptionsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    files: List[FilesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    ref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    priority: StepComplexTypePriority = field(
        default=StepComplexTypePriority.DEFAULT,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class TestComplexType:
    """
    :ivar meta:
    :ivar product:
    :ivar expected_result:
    :ivar id:
    """
    class Meta:
        name = "testComplexType"

    meta: List[MetaComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    product: List[ProductComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    expected_result: List[ExpectedResultComplexType] = field(
        default_factory=list,
        metadata={
            "name": "expectedResult",
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Results(ResultsComplexType):
    class Meta:
        name = "results"
        namespace = "http://momotor.org/1.0"


@dataclass
class StepsComplexType:
    """
    :ivar step:
    :ivar options:
    :ivar checklets:
    """
    class Meta:
        name = "stepsComplexType"

    step: List[StepComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    options: List[OptionsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    checklets: List[CheckletsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )


@dataclass
class TestResultComplexType:
    """
    :ivar results:
    """
    class Meta:
        name = "testResultComplexType"

    results: List[ResultsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )


@dataclass
class TestsComplexType:
    """
    :ivar expected_result:
    :ivar expect:
    :ivar files:
    :ivar properties:
    :ivar test:
    """
    class Meta:
        name = "testsComplexType"

    expected_result: List[ExpectedResultComplexType] = field(
        default_factory=list,
        metadata={
            "name": "expectedResult",
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    expect: List[ExpectComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    files: List[FilesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    properties: List[PropertiesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    test: List[TestComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )


@dataclass
class RecipeComplexType:
    """
    :ivar meta:
    :ivar options:
    :ivar checklets:
    :ivar files:
    :ivar steps:
    :ivar tests:
    :ivar id:
    """
    class Meta:
        name = "recipeComplexType"

    meta: List[MetaComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    options: List[OptionsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    checklets: List[CheckletsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    files: List[FilesComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    steps: List[StepsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    tests: List[TestsComplexType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://momotor.org/1.0",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Testresult(TestResultComplexType):
    class Meta:
        name = "testresult"
        namespace = "http://momotor.org/1.0"


@dataclass
class Recipe(RecipeComplexType):
    class Meta:
        name = "recipe"
        namespace = "http://momotor.org/1.0"
