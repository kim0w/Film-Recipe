"""이미지 처리 파이프라인"""
import numpy as np
from PIL import Image, ImageFile
from typing import Dict, Optional
from pathlib import Path
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

# PIL이 잘린 이미지도 로드할 수 있도록 설정
ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImageProcessor:
    """필름 시뮬레이션 이미지 처리 클래스"""

    # 클래스 상수
    MAX_DIMENSION = 4096  # 4K 해상도 제한
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    SUPPORTED_FORMATS = {'JPEG', 'PNG', 'TIFF', 'BMP'}

    # 그레인 캐시
    _grain_cache: Dict[str, np.ndarray] = {}

    @classmethod
    def apply_film_simulation(
        cls,
        input_path: str,
        output_path: str,
        film_recipe: Dict
    ) -> str:
        """
        필름 시뮬레이션 적용

        파이프라인:
        1. 이미지 로드 및 검증
        2. Gamma Decode (sRGB → Linear RGB)
        3. 톤 커브 적용
        4. 그레인 오버레이
        5. Gamma Encode (Linear RGB → sRGB)
        6. 저장

        Args:
            input_path (str): 입력 이미지 경로
            output_path (str): 출력 이미지 경로
            film_recipe (Dict): 필름 레시피 정보

        Returns:
            str: 출력 파일 경로

        Raises:
            ValueError: 입력 검증 실패
            IOError: 파일 읽기/쓰기 실패
            RuntimeError: 이미지 처리 실패
        """
        input_file = Path(input_path)
        output_file = Path(output_path)

        # 입력 파일 검증
        cls._validate_input_file(input_file)

        # 출력 디렉토리 생성
        output_file.parent.mkdir(parents=True, exist_ok=True)

        img = None
        try:
            # 1. 이미지 로드 (context manager 사용)
            with Image.open(input_file) as img_temp:
                # 이미지 복사 (context manager 밖에서 사용하기 위해)
                img = img_temp.copy()

            # 2. 대용량 이미지 처리 (메모리 효율성)
            if max(img.size) > cls.MAX_DIMENSION:
                logger.warning(
                    f"Large image detected ({img.size}), "
                    f"resizing to {cls.MAX_DIMENSION}px"
                )
                ratio = cls.MAX_DIMENSION / max(img.size)
                new_size = tuple(int(dim * ratio) for dim in img.size)
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            # 3. RGBA → RGB 변환 (PNG 알파 채널 처리)
            img = cls._convert_to_rgb(img)

            # 4. Numpy 배열로 변환 (0~1 범위)
            img_array = np.array(img, dtype=np.float32) / 255.0

            # 5. Gamma Decode (sRGB → Linear RGB)
            img_linear = cls._gamma_decode(img_array)

            # 6. 톤 커브 적용 (필름별 특성)
            img_toned = cls._apply_tone_curve(img_linear, film_recipe)

            # 7. 그레인 오버레이
            img_grain = cls._apply_grain_overlay(img_toned, film_recipe)

            # 8. Gamma Encode (Linear RGB → sRGB)
            img_srgb = cls._gamma_encode(img_grain)

            # 9. 0~255 범위로 변환 및 클리핑
            img_final = (np.clip(img_srgb, 0, 1) * 255).astype(np.uint8)

            # 10. PIL Image로 변환 및 저장
            output_img = Image.fromarray(img_final, mode='RGB')
            output_img.save(
                output_file,
                format='JPEG',
                quality=95,
                optimize=True,
                subsampling=0  # 최고 품질 chroma subsampling
            )

            logger.info(f"Image processed successfully: {output_file}")
            return str(output_file)

        except ValueError as e:
            logger.error(f"Validation error: {e}")
            raise
        except IOError as e:
            logger.error(f"File I/O error: {e}")
            raise
        except Exception as e:
            logger.error(f"Image processing failed: {e}", exc_info=True)
            raise RuntimeError(f"Image processing failed: {e}") from e
        finally:
            # 리소스 정리
            if img is not None:
                img.close()

    @classmethod
    def _validate_input_file(cls, file_path: Path) -> None:
        """
        입력 파일 검증

        Args:
            file_path (Path): 파일 경로

        Raises:
            ValueError: 파일 검증 실패
        """
        # 파일 존재 확인
        if not file_path.exists():
            raise ValueError(f"Input file does not exist: {file_path}")

        # 파일인지 확인
        if not file_path.is_file():
            raise ValueError(f"Input path is not a file: {file_path}")

        # 파일 크기 확인
        file_size = file_path.stat().st_size
        if file_size > cls.MAX_FILE_SIZE:
            raise ValueError(
                f"File too large: {file_size / 1024 / 1024:.2f}MB "
                f"(max {cls.MAX_FILE_SIZE / 1024 / 1024}MB)"
            )

        # 파일 형식 확인 (확장자 기반)
        suffix = file_path.suffix.upper().lstrip('.')
        if suffix not in cls.SUPPORTED_FORMATS and suffix not in {'JPG'}:
            raise ValueError(
                f"Unsupported file format: {suffix}. "
                f"Supported: {', '.join(cls.SUPPORTED_FORMATS)}"
            )

    @staticmethod
    def _convert_to_rgb(img: Image.Image) -> Image.Image:
        """
        이미지를 RGB로 변환

        Args:
            img (Image.Image): 입력 이미지

        Returns:
            Image.Image: RGB 이미지
        """
        if img.mode == 'RGBA':
            # 흰 배경에 알파 채널 합성
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            return background
        elif img.mode == 'P':
            # 팔레트 모드 → RGB
            return img.convert('RGB')
        elif img.mode != 'RGB':
            return img.convert('RGB')
        return img

    @staticmethod
    def _gamma_decode(img: np.ndarray) -> np.ndarray:
        """
        Gamma Decode: sRGB → Linear RGB (정확한 sRGB 공식 사용)

        sRGB는 piecewise 함수:
        - V <= 0.04045: V / 12.92
        - V > 0.04045: ((V + 0.055) / 1.055) ^ 2.4

        Args:
            img (np.ndarray): sRGB 이미지 (0~1)

        Returns:
            np.ndarray: Linear RGB 이미지
        """
        # 간단한 gamma 2.2 사용 (성능 고려)
        # 정확한 sRGB 변환이 필요하면 piecewise 함수 사용
        return np.where(
            img <= 0.04045,
            img / 12.92,
            np.power((img + 0.055) / 1.055, 2.4)
        )

    @staticmethod
    def _gamma_encode(img: np.ndarray) -> np.ndarray:
        """
        Gamma Encode: Linear RGB → sRGB (정확한 sRGB 공식 사용)

        sRGB는 piecewise 함수:
        - V <= 0.0031308: V * 12.92
        - V > 0.0031308: 1.055 * V^(1/2.4) - 0.055

        Args:
            img (np.ndarray): Linear RGB 이미지 (0~1)

        Returns:
            np.ndarray: sRGB 이미지
        """
        return np.where(
            img <= 0.0031308,
            img * 12.92,
            1.055 * np.power(img, 1.0 / 2.4) - 0.055
        )

    @classmethod
    def _apply_tone_curve(cls, img: np.ndarray, film_recipe: Dict) -> np.ndarray:
        """
        필름별 톤 커브 적용

        MVP 단계에서는 간단한 S-curve 적용
        향후 실제 Characteristic Curves 데이터 사용 예정

        Args:
            img (np.ndarray): Linear RGB 이미지
            film_recipe (Dict): 필름 레시피 정보

        Returns:
            np.ndarray: 톤 커브 적용된 이미지
        """
        film_name = film_recipe.get('film_name', '')
        film_type = film_recipe.get('type', 'color')

        # 이미지 복사 (원본 보존)
        img_result = img.copy()

        # Velvia 50: 초고채도 (강한 S-curve + 채도 증가)
        if 'Velvia' in film_name:
            img_result = cls._s_curve(img_result, strength=0.3)
            img_result = np.clip(img_result * 1.15, 0, 1)

        # Provia 100F: 자연스러운 색감 (약한 S-curve)
        elif 'Provia' in film_name:
            img_result = cls._s_curve(img_result, strength=0.15)
            img_result = np.clip(img_result * 1.05, 0, 1)

        # Portra 400: 부드러운 피부톤 (매우 약한 S-curve)
        elif 'Portra' in film_name:
            img_result = cls._s_curve(img_result, strength=0.12)
            # 피부톤 강조 (Red/Green 채널 약간 증가)
            img_result[:, :, 0] = np.clip(img_result[:, :, 0] * 1.03, 0, 1)
            img_result[:, :, 1] = np.clip(img_result[:, :, 1] * 1.02, 0, 1)

        # Vision3 500T: 시네마틱 톤 (약한 S-curve + 약간 어둡게)
        elif 'Vision3' in film_name:
            img_result = cls._s_curve(img_result, strength=0.18)
            img_result = np.clip(img_result * 0.98, 0, 1)

        # T-Max 100: 흑백 변환 + 강한 대비
        elif 'T-Max' in film_name or film_type == 'bw':
            # 흑백 변환 (Rec. 709 가중치)
            bw_weight_r = film_recipe.get('bw_weight_r', 0.299)
            bw_weight_g = film_recipe.get('bw_weight_g', 0.587)
            bw_weight_b = film_recipe.get('bw_weight_b', 0.114)

            gray = (img_result[:, :, 0] * bw_weight_r +
                   img_result[:, :, 1] * bw_weight_g +
                   img_result[:, :, 2] * bw_weight_b)

            # 3채널로 복사 (흑백 이미지)
            img_result = np.stack([gray] * 3, axis=-1)

            # 강한 대비 (S-curve)
            img_result = cls._s_curve(img_result, strength=0.25)

        # 기타: 기본 S-curve
        else:
            img_result = cls._s_curve(img_result, strength=0.10)

        return img_result

    @staticmethod
    def _s_curve(img: np.ndarray, strength: float = 0.2) -> np.ndarray:
        """
        S-curve 톤 커브 적용 (대비 증가)

        공식: y = x + strength * (x - x^3)

        Args:
            img (np.ndarray): 입력 이미지 (0~1)
            strength (float): S-curve 강도 (0~1)

        Returns:
            np.ndarray: S-curve 적용된 이미지
        """
        x = img
        y = x + strength * (x - x ** 3)
        return np.clip(y, 0, 1)

    @classmethod
    def _apply_grain_overlay(cls, img: np.ndarray, film_recipe: Dict) -> np.ndarray:
        """
        필름 그레인 오버레이 적용 (캐싱 사용)

        Args:
            img (np.ndarray): Linear RGB 이미지 (0~1)
            film_recipe (Dict): 필름 레시피 정보

        Returns:
            np.ndarray: 그레인 적용된 이미지
        """
        try:
            film_name = film_recipe.get('film_name', '')
            grain_intensity = film_recipe.get('grain_intensity', 0.3)

            # 그레인 강도가 0이면 스킵
            if grain_intensity <= 0.0:
                return img

            # 필름별 그레인 파일 선택
            grain_file = cls._get_grain_file(film_name)

            # 그레인 텍스처 로드 (캐싱 사용)
            grain_array = cls._load_grain_texture(grain_file)

            if grain_array is None:
                logger.warning(f"Grain file not found: {grain_file}, skipping grain overlay")
                return img

            # 이미지 크기에 맞게 리사이즈
            target_size = (img.shape[1], img.shape[0])  # (width, height)

            # 원본 그레인 크기와 다르면 리사이즈
            if grain_array.shape[:2] != (target_size[1], target_size[0]):
                grain_resized = Image.fromarray((grain_array * 255).astype(np.uint8))
                grain_resized = grain_resized.resize(
                    target_size,
                    Image.Resampling.LANCZOS
                )
                grain_array = np.array(grain_resized, dtype=np.float32) / 255.0

            # 그레인을 3채널로 확장
            grain_3ch = np.stack([grain_array] * 3, axis=-1)

            # Overlay blend mode (정확한 Photoshop Overlay 공식)
            # if base < 0.5: 2 * base * blend
            # else: 1 - 2 * (1 - base) * (1 - blend)
            result = np.where(
                img < 0.5,
                2 * img * grain_3ch,
                1 - 2 * (1 - img) * (1 - grain_3ch)
            )

            # 강도 조절 (원본과 블렌드)
            result = img * (1 - grain_intensity) + result * grain_intensity

            return np.clip(result, 0, 1)

        except Exception as e:
            logger.error(f"Grain overlay failed: {e}", exc_info=True)
            return img

    @classmethod
    def _load_grain_texture(cls, grain_file: str) -> Optional[np.ndarray]:
        """
        그레인 텍스처 로드 (캐싱 사용)

        Args:
            grain_file (str): 그레인 파일명

        Returns:
            Optional[np.ndarray]: 그레인 배열 (0~1) 또는 None
        """
        # 캐시 확인
        if grain_file in cls._grain_cache:
            return cls._grain_cache[grain_file]

        try:
            from backend.config import Config

            grain_folder = Config.BASE_DIR / 'data' / 'grain_overlays'
            grain_path = grain_folder / grain_file

            if not grain_path.exists():
                return None

            # 그레인 이미지 로드
            with Image.open(grain_path) as grain_img:
                grain_array = np.array(
                    grain_img.convert('L'),
                    dtype=np.float32
                ) / 255.0

            # 캐시에 저장
            cls._grain_cache[grain_file] = grain_array

            logger.debug(f"Grain texture loaded and cached: {grain_file}")

            return grain_array

        except Exception as e:
            logger.error(f"Failed to load grain texture {grain_file}: {e}")
            return None

    @staticmethod
    def _get_grain_file(film_name: str) -> str:
        """
        필름명에 따라 그레인 파일 선택

        Args:
            film_name (str): 필름명

        Returns:
            str: 그레인 파일명
        """
        if 'Velvia' in film_name:
            return 'grain_rms_9.png'
        elif 'Provia' in film_name:
            return 'grain_rms_8.png'
        elif 'Portra' in film_name:
            return 'grain_pgi_37.png'
        elif 'Vision3' in film_name:
            return 'grain_cine.png'
        elif 'T-Max' in film_name:
            return 'grain_pgi_25.png'
        else:
            # 기본 그레인
            return 'grain_rms_9.png'
