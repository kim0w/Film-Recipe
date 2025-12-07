"""필름 그레인 텍스처 생성 유틸리티"""
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from pathlib import Path
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class GrainGenerator:
    """필름 그레인 텍스처를 생성하는 클래스"""

    @staticmethod
    def generate_grain_texture(
        size: Tuple[int, int] = (2048, 2048),
        grain_size: int = 9,
        intensity: float = 0.5,
        output_path: Optional[str] = None,
        random_seed: Optional[int] = None
    ) -> Image.Image:
        """
        필름 그레인 텍스처 생성

        Args:
            size (Tuple[int, int]): 텍스처 크기 (width, height)
            grain_size (int): 그레인 입자 크기 (RMS Granularity 또는 PGI 값, 1-100)
            intensity (float): 그레인 강도 (0.0 ~ 1.0)
            output_path (Optional[str]): 저장 경로 (선택적)
            random_seed (Optional[int]): 랜덤 시드 (재현성용, 선택적)

        Returns:
            Image.Image: 그레인 텍스처 이미지 (grayscale)

        Raises:
            ValueError: 입력 파라미터가 유효하지 않을 경우
        """
        # 입력 검증
        if not isinstance(size, tuple) or len(size) != 2:
            raise ValueError(f"Size must be a tuple of 2 integers, got: {size}")

        if size[0] <= 0 or size[1] <= 0:
            raise ValueError(f"Size dimensions must be positive, got: {size}")

        if not (1 <= grain_size <= 100):
            raise ValueError(f"grain_size must be between 1 and 100, got: {grain_size}")

        if not (0.0 <= intensity <= 1.0):
            raise ValueError(f"intensity must be between 0.0 and 1.0, got: {intensity}")

        logger.debug(f"Generating grain: size={size}, grain_size={grain_size}, intensity={intensity}")

        # 1. 랜덤 노이즈 생성
        if random_seed is not None:
            np.random.seed(random_seed)
        noise = np.random.randn(size[1], size[0])

        # 2. 정규화 (0~1 범위)
        noise_min, noise_max = noise.min(), noise.max()
        noise_range = noise_max - noise_min

        # Division by zero 방지
        if noise_range < 1e-10:
            logger.warning("Noise range too small, using uniform gray")
            noise = np.full(size, 0.5)
        else:
            noise = (noise - noise_min) / noise_range

        # 3. 강도 조절 (0.5를 중심으로 ±intensity)
        noise = 0.5 + (noise - 0.5) * intensity

        # 4. Gaussian blur로 입자 크기 조절
        # grain_size가 클수록 blur를 많이 줘서 큰 입자감 생성
        sigma = grain_size / 10.0
        noise_blurred = gaussian_filter(noise, sigma=sigma)

        # 5. 다시 정규화
        blurred_min, blurred_max = noise_blurred.min(), noise_blurred.max()
        blurred_range = blurred_max - blurred_min

        # Division by zero 방지
        if blurred_range < 1e-10:
            logger.warning("Blurred noise range too small, using uniform gray")
            noise_blurred = np.full(size, 0.5)
        else:
            noise_blurred = (noise_blurred - blurred_min) / blurred_range

        # 6. 8-bit 이미지로 변환
        grain_array = (noise_blurred * 255).astype(np.uint8)
        grain_img = Image.fromarray(grain_array, mode='L')

        # 7. 저장 (선택적)
        if output_path:
            try:
                # 출력 디렉토리 확인 및 생성
                output_path_obj = Path(output_path)
                output_path_obj.parent.mkdir(parents=True, exist_ok=True)

                grain_img.save(str(output_path))
                logger.info(f"Grain texture saved: {output_path}")
            except Exception as e:
                logger.error(f"Failed to save grain texture to {output_path}: {e}", exc_info=True)
                raise IOError(f"Failed to save grain texture: {e}")

        return grain_img

    @staticmethod
    def generate_all_mvp_grains(output_folder: Path):
        """
        MVP 5개 필름의 그레인 텍스처 일괄 생성

        Args:
            output_folder (Path): 출력 폴더 경로

        Raises:
            IOError: 출력 폴더 생성 또는 파일 저장 실패 시
        """
        try:
            output_folder.mkdir(parents=True, exist_ok=True)
            logger.info(f"Output folder created/verified: {output_folder}")
        except Exception as e:
            logger.error(f"Failed to create output folder {output_folder}: {e}", exc_info=True)
            raise IOError(f"Failed to create output folder: {e}")

        # MVP 필름별 그레인 파라미터
        # (grain_size, intensity, random_seed)
        grains = {
            'grain_rms_9':  (9, 0.35, 101),   # Velvia 50 (RMS 9)
            'grain_rms_8':  (8, 0.30, 102),   # Provia 100F (RMS 8)
            'grain_pgi_37': (37, 0.35, 103),  # Portra 400 (PGI 37)
            'grain_pgi_25': (25, 0.15, 104),  # T-Max 100 (PGI < 25)
            'grain_cine':   (15, 0.25, 105),  # Vision3 500T (시네마 그레인)
        }

        success_count = 0
        failed_grains = []

        for name, (size, intensity, seed) in grains.items():
            output_path = output_folder / f"{name}.png"

            try:
                logger.info(f"Generating {name} (size={size}, intensity={intensity}, seed={seed})...")

                GrainGenerator.generate_grain_texture(
                    size=(2048, 2048),
                    grain_size=size,
                    intensity=intensity,
                    output_path=str(output_path),
                    random_seed=seed
                )

                success_count += 1

            except Exception as e:
                logger.error(f"Failed to generate {name}: {e}", exc_info=True)
                failed_grains.append(name)

        # 결과 로깅
        if failed_grains:
            logger.warning(
                f"Generated {success_count}/{len(grains)} grain textures. "
                f"Failed: {', '.join(failed_grains)}"
            )
        else:
            logger.info(f"All {success_count} grain textures generated successfully in {output_folder}")


# 메인 실행 (독립 실행 시)
if __name__ == '__main__':
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

    from backend.config import Config

    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # 그레인 폴더 경로
    grain_folder = Config.BASE_DIR / 'data' / 'grain_overlays'

    # 그레인 텍스처 생성
    GrainGenerator.generate_all_mvp_grains(grain_folder)

    print("\n🎉 Grain texture generation completed!")
    print(f"📁 Output folder: {grain_folder}")
