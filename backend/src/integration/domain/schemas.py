from typing import Literal, TypedDict

from pydantic import BaseModel, Field


class TextVoice(BaseModel):
    class ElevenLabsSettings(BaseModel):
        model: Literal[
            "eleven_monolingual_v1", "eleven_multilingual_v1", "eleven_multilingual_v2", "eleven_turbo_v2", "eleven_turbo_v2_5"]
        similarity_boost: float | None = Field(default=None, ge=0, le=1,
                                               description="Controls how similar the generated speech should be to the original voice")
        stability: float | None = Field(default=None, ge=0, le=1,
                                        description="Controls the stability of the voice generation. Higher values result in more consistent and stable output")
        style: float | None = Field(default=None, ge=0, le=1,
                                    description="Controls the style intensity of the generated speech")

    type: Literal["text"] = "text"
    voice_id: str
    input_text: str
    speed: float = Field(default=1.0, ge=0.5, le=1.5)
    pitch: int = Field(default=0, ge=-50, le=50)
    emotion: str | None = None
    locale: str | None = None
    elevenlabs_settings: ElevenLabsSettings | None = None


class AudioVoice(BaseModel):
    type: Literal["audio"] = "audio"
    audio_url: str | None = None
    audio_asset_id: str | None = None


class SilenceVoice(BaseModel):
    type: Literal["silence"] = "silence"
    duration: float = Field(default=1.0, ge=1, le=100)


class Background(BaseModel):
    type: Literal["color", "image", "video"]
    value: str | None = Field(default=None, description="Color for type=color")


class AvatarCharacter(BaseModel):
    type: Literal["avatar"] = "avatar"
    avatar_id: str
    scale: float = Field(default=1.0, ge=0, le=5)
    avatar_style: Literal["normal", "circle", "closeUp"]
    offset: TypedDict("Coordinates", {"x": float, "y": float}) | None = None
    matting: bool | None = None
    circle_background_color: str | None = None


class TalkingPhotoCharacter(BaseModel):
    type: Literal["talking_photo"] = "talking_photo"
    talking_photo_id: str
    talking_photo_style: Literal["square", "circle"] | None = None
    scale: float = Field(default=1.0, ge=0, le=2)
    offset: TypedDict("Coordinates", {"x": float, "y": float}) | None = None
    talking_style: Literal["stable", "expressive"] | None = None
    expression: Literal["defauilt", "happy"] | None = None
    super_resolution: bool | None = None
    matting: bool | None = None
    circle_background_color: str | None = None


class HeygenRunRequest(BaseModel):
    class VideoInput(BaseModel):
        character: AvatarCharacter | TalkingPhotoCharacter | None = None
        voice: TextVoice | AudioVoice | SilenceVoice
        background: Background | None = None

    video_inputs: list[VideoInput]
    dimension: TypedDict("Dimension", {"width": int, "height": int}) = Field(default_factory=lambda: {"width": 1280, "height": 720})


class HeygenRunResponse(BaseModel):
    class Data(BaseModel):
        video_id: str

    data: Data


class HeygenStatusResponse(BaseModel):
    class Data(BaseModel):
        duration: float | None = None
        error: dict | None = None
        gif_url: str | None = None
        id: str
        status: Literal["processing", "completed", "failed", "pending"]
        thumbnail_url: str | None = None
        video_url: str | None = None

    data: Data


class HeygenVoicesResponse(BaseModel):
    class Data(BaseModel):
        class Voice(BaseModel):
            voice_id: str
            language: str
            gender: str
            name: str
            preview_audio: str
            support_pause: bool
            emotion_support: bool
            support_locale: bool

        voices: list[Voice]

    data: Data


class HeygenAvatarsResponse(BaseModel):
    class Data(BaseModel):
        class Avatar(BaseModel):
            avatar_id: str
            avatar_name: str
            preview_image_url: str
            preview_video_url: str
            gender: str
            premium: bool

        avatars: list[Avatar]

    data: Data
