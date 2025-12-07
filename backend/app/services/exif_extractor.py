"""EXIF 메타데이터 추출 서비스"""
import exifread
import logging
from typing import Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class EXIFExtractor:
    """이미지 파일에서 EXIF 메타데이터를 추출하는 클래스"""

    @staticmethod
    def extract(image_path: str) -> Dict:
        """
        이미지 파일에서 EXIF 데이터 추출

        Args:
            image_path (str): 이미지 파일 경로

        Returns:
            Dict: EXIF 데이터 딕셔너리
        """
        # 파일 경로 검증
        path = Path(image_path)
        if not path.exists():
            logger.warning(f"파일을 찾을 수 없습니다: {image_path}")
            return EXIFExtractor._default_exif()

        if not path.is_file():
            logger.warning(f"유효한 파일이 아닙니다: {image_path}")
            return EXIFExtractor._default_exif()

        try:
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f, details=False)
                logger.debug(f"EXIF tags extracted from {path.name}: {len(tags)} tags")

            # 모든 EXIF 데이터 추출
            exif_data = {
                'iso': EXIFExtractor._extract_iso(tags),
                'shutter_speed': EXIFExtractor._extract_shutter_speed(tags),
                'aperture': EXIFExtractor._extract_aperture(tags),
                'focal_length': EXIFExtractor._extract_focal_length(tags),
                'white_balance': EXIFExtractor._extract_white_balance(tags),
                'color_temperature': EXIFExtractor._extract_color_temperature(tags),
                'camera_make': EXIFExtractor._extract_camera_make(tags),
                'camera_model': EXIFExtractor._extract_camera_model(tags),
                'lens_model': EXIFExtractor._extract_lens_model(tags),
                'datetime': EXIFExtractor._extract_datetime(tags),
            }

            return exif_data

        except FileNotFoundError:
            logger.warning(f"파일을 찾을 수 없습니다: {image_path}")
            return EXIFExtractor._default_exif()
        except Exception as e:
            logger.error(f"EXIF 추출 중 오류 발생: {str(e)}")
            return EXIFExtractor._default_exif()

    @staticmethod
    def _extract_iso(tags) -> int:
        """ISO 감도 추출"""
        if 'EXIF ISOSpeedRatings' in tags:
            try:
                iso_value = str(tags['EXIF ISOSpeedRatings'])
                return int(iso_value)
            except (ValueError, TypeError):
                pass

        # ISO 정보가 없으면 기본값 200
        return 200

    @staticmethod
    def _extract_shutter_speed(tags) -> float:
        """
        셔터 속도 추출 (초 단위)

        Returns:
            float: 셔터 속도 (초). 예: 1/125s = 0.008
        """
        if 'EXIF ExposureTime' in tags:
            try:
                value = str(tags['EXIF ExposureTime'])

                # 분수 형태 (예: "1/125")
                if '/' in value:
                    numerator, denominator = value.split('/')
                    return float(numerator) / float(denominator)

                # 소수 형태
                return float(value)

            except (ValueError, TypeError, ZeroDivisionError):
                pass

        # 기본값: 1/125s
        return 0.008

    @staticmethod
    def _extract_aperture(tags) -> float:
        """
        조리개 값 추출 (F-number)

        Returns:
            float: 조리개 값. 예: f/5.6
        """
        if 'EXIF FNumber' in tags:
            try:
                value = str(tags['EXIF FNumber'])

                # 분수 형태 (예: "28/5" = 5.6)
                if '/' in value:
                    numerator, denominator = value.split('/')
                    return round(float(numerator) / float(denominator), 1)

                # 소수 형태
                return round(float(value), 1)

            except (ValueError, TypeError, ZeroDivisionError):
                pass

        # MaxAperture로 시도
        if 'EXIF MaxApertureValue' in tags:
            try:
                value = str(tags['EXIF MaxApertureValue'])
                if '/' in value:
                    numerator, denominator = value.split('/')
                    apex_value = float(numerator) / float(denominator)
                    # APEX → F-number 변환: F = 2^(APEX/2)
                    f_number = 2 ** (apex_value / 2)
                    return round(f_number, 1)
            except (ValueError, TypeError, ZeroDivisionError):
                pass

        # 기본값: f/5.6
        return 5.6

    @staticmethod
    def _extract_focal_length(tags) -> Optional[int]:
        """초점 거리 추출 (mm)"""
        if 'EXIF FocalLength' in tags:
            try:
                value = str(tags['EXIF FocalLength'])

                if '/' in value:
                    numerator, denominator = value.split('/')
                    return int(float(numerator) / float(denominator))

                return int(float(value))

            except (ValueError, TypeError, ZeroDivisionError):
                pass

        return 50  # 기본값: 50mm

    @staticmethod
    def _extract_white_balance(tags) -> str:
        """화이트 밸런스 추출"""
        if 'EXIF WhiteBalance' in tags:
            wb_value = str(tags['EXIF WhiteBalance'])

            # 0 = Auto, 1 = Manual
            if wb_value == '0':
                return 'Auto'
            elif wb_value == '1':
                return 'Manual'

        # LightSource 태그 확인
        if 'EXIF LightSource' in tags:
            light_source = str(tags['EXIF LightSource'])

            light_source_map = {
                '1': 'Daylight',
                '2': 'Fluorescent',
                '3': 'Tungsten',
                '4': 'Flash',
                '9': 'Fine Weather',
                '10': 'Cloudy',
                '11': 'Shade',
                '17': 'Standard Light A',
                '18': 'Standard Light B',
                '19': 'Standard Light C',
            }

            return light_source_map.get(light_source, 'Auto')

        return 'Auto'

    @staticmethod
    def _extract_color_temperature(tags) -> int:
        """
        색온도 추출 (Kelvin)

        화이트밸런스에서 추정
        """
        wb = EXIFExtractor._extract_white_balance(tags)

        # 화이트밸런스 → 색온도 매핑
        wb_to_temp = {
            'Tungsten': 3200,
            'Fluorescent': 4000,
            'Daylight': 5500,
            'Cloudy': 6500,
            'Shade': 7500,
            'Flash': 5500,
            'Fine Weather': 5500,
            'Auto': 5500,
            'Manual': 5500,
        }

        return wb_to_temp.get(wb, 5500)

    @staticmethod
    def _extract_camera_make(tags) -> str:
        """카메라 제조사 추출"""
        if 'Image Make' in tags:
            return str(tags['Image Make']).strip()
        return 'Unknown'

    @staticmethod
    def _extract_camera_model(tags) -> str:
        """카메라 모델 추출"""
        if 'Image Model' in tags:
            return str(tags['Image Model']).strip()
        return 'Unknown'

    @staticmethod
    def _extract_lens_model(tags) -> Optional[str]:
        """렌즈 모델 추출"""
        if 'EXIF LensModel' in tags:
            return str(tags['EXIF LensModel']).strip()
        return None

    @staticmethod
    def _extract_datetime(tags) -> Optional[str]:
        """촬영 날짜/시간 추출"""
        if 'EXIF DateTimeOriginal' in tags:
            return str(tags['EXIF DateTimeOriginal'])
        if 'Image DateTime' in tags:
            return str(tags['Image DateTime'])
        return None

    @staticmethod
    def _default_exif() -> Dict:
        """
        기본 EXIF 데이터 반환 (추출 실패 시)

        일반적인 촬영 조건 가정
        """
        return {
            'iso': 200,
            'shutter_speed': 0.008,  # 1/125s
            'aperture': 5.6,
            'focal_length': 50,
            'white_balance': 'Auto',
            'color_temperature': 5500,
            'camera_make': 'Unknown',
            'camera_model': 'Unknown',
            'lens_model': None,
            'datetime': None,
        }
