import dataclasses
from dataclasses import dataclass
from typing import Union, Any
from dataclasses_json import dataclass_json
from streamlit_timeline import timeline

Color = str
URL = str

immutable = dataclass(frozen=True)


@dataclass_json
class JSON:
    def __getattribute__(self, name: str) -> Any:
        attributes = super().__getattribute__(name)
        if name == "__dataclass_fields__":
            for key, field in list(attributes.items()):
                if field.default is None and super().__getattribute__(key) is None:
                    del attributes[key]
        return attributes

    def __str__(self):
        return self.to_json()


@immutable
class Text(JSON):
    headline: str = None
    text: str = None


@immutable
class Media(JSON):
    url: URL
    caption: str = None
    credit: str = None
    thumbnail: URL = None
    title: str = None
    alt: str = None
    link: URL = None
    link_target: str = None


@immutable
class DateTime(JSON):
    year: str
    month: str = None
    day: str = None
    hour: str = None
    minute: str = None
    second: str = None
    millisecond: str = None
    display_date: str = None


@immutable
class Slide(JSON):
    start_date: DateTime
    end_date: DateTime = None
    text: Text = None
    media: Media = None
    group: str = None
    display_date: str = None
    background: Union[Color, URL] = None
    autolink: bool = None
    unique_id: str = None


@dataclass
class Era(JSON):
    start_date: DateTime
    end_date: DateTime = None
    text: Text = None


@dataclass
class Timeline(JSON):
    events: list[Slide]
    height: int = None
    title: Slide = None
    erase: list[Slide] = None
    scale: str = None

    def __post_init__(self):
        timeline(str(self), height=self.height)
