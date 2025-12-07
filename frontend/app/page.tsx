"use client";

import { useState } from "react";
import axios, { AxiosError } from "axios";
import { useDropzone } from "react-dropzone";

// API URL from environment variable or fallback to localhost
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000/api";
const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB

interface Film {
  film_id: number;
  film_name: string;
  manufacturer: string;
  tier: string;
  score: number;
  reason: string;
  iso_base: number;
  type: string;
}

interface ProcessedResult {
  film_id: number;
  film_name: string;
  output_url?: string;
  status: string;
  error?: string;
  processing_time?: number;
}

export default function Home() {
  const [jobId, setJobId] = useState("");
  const [films, setFilms] = useState<Film[]>([]);
  const [results, setResults] = useState<ProcessedResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onDrop = async (acceptedFiles: File[]) => {
    // 에러 초기화
    setError(null);

    // 파일 선택 확인
    if (acceptedFiles.length === 0) {
      setError("이미지 파일을 선택해주세요");
      return;
    }

    // 파일 크기 검증
    const file = acceptedFiles[0];
    if (file.size > MAX_FILE_SIZE) {
      setError(
        `파일 크기가 너무 큽니다. 최대 ${MAX_FILE_SIZE / 1024 / 1024}MB까지 업로드 가능합니다.`
      );
      return;
    }

    const formData = new FormData();
    formData.append("images", file);

    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      // 응답 검증
      if (!res.data || !res.data.job_id || !res.data.images || res.data.images.length === 0) {
        throw new Error("서버 응답이 올바르지 않습니다");
      }

      const uploadedImage = res.data.images[0];
      if (!uploadedImage.matched_films || uploadedImage.matched_films.length === 0) {
        throw new Error("매칭된 필름을 찾을 수 없습니다");
      }

      setJobId(res.data.job_id);
      setFilms(uploadedImage.matched_films);
      setUploadedFile(file.name);
      console.log("Upload successful:", res.data);
    } catch (err) {
      console.error("Upload error:", err);

      // 에러 메시지 구체화
      if (axios.isAxiosError(err)) {
        const axiosError = err as AxiosError<{ error?: string; message?: string }>;
        if (axiosError.response) {
          const errorMsg = axiosError.response.data?.error || axiosError.response.data?.message;
          setError(errorMsg || `업로드 실패: ${axiosError.response.status}`);
        } else if (axiosError.request) {
          setError("서버에 연결할 수 없습니다. 네트워크를 확인해주세요.");
        } else {
          setError("업로드 중 오류가 발생했습니다.");
        }
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("업로드 실패. 다시 시도해주세요.");
      }
    } finally {
      setLoading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxFiles: 1,
    accept: {
      "image/*": [".jpg", ".jpeg", ".png"],
    },
  });

  const processImages = async () => {
    // 에러 초기화
    setError(null);

    // 입력 검증
    if (!jobId || films.length === 0) {
      setError("먼저 이미지를 업로드해주세요");
      return;
    }

    setLoading(true);
    try {
      const filmIds = films.map((f) => f.film_id);
      const res = await axios.post(`${API_BASE_URL}/process`, {
        job_id: jobId,
        film_ids: filmIds,
      });

      // 응답 검증
      if (!res.data || !res.data.results) {
        throw new Error("서버 응답이 올바르지 않습니다");
      }

      setResults(res.data.results);
      console.log("Processing successful:", res.data);

      // 일부 실패 시 경고 표시
      const failedCount = res.data.failed || 0;
      if (failedCount > 0) {
        setError(`${failedCount}개의 필름 처리가 실패했습니다. 성공: ${res.data.success}개`);
      }
    } catch (err) {
      console.error("Processing error:", err);

      // 에러 메시지 구체화
      if (axios.isAxiosError(err)) {
        const axiosError = err as AxiosError<{ error?: string; message?: string }>;
        if (axiosError.response) {
          const errorMsg = axiosError.response.data?.error || axiosError.response.data?.message;
          setError(errorMsg || `처리 실패: ${axiosError.response.status}`);
        } else if (axiosError.request) {
          setError("서버에 연결할 수 없습니다. 네트워크를 확인해주세요.");
        } else {
          setError("처리 중 오류가 발생했습니다.");
        }
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("처리 실패. 다시 시도해주세요.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-4 md:p-8 bg-gradient-to-b from-gray-50 to-gray-100">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-5xl font-bold text-gray-900 mb-3">
            Film Recipe
          </h1>
          <p className="text-xl text-gray-600">
            디지털 사진에 아날로그 필름 효과를 적용하세요
          </p>
        </div>

        {/* Upload Zone */}
        <div
          {...getRootProps()}
          className={`border-3 border-dashed rounded-2xl p-16 text-center cursor-pointer transition-all mb-8 ${
            isDragActive
              ? "border-blue-500 bg-blue-50"
              : "border-gray-300 bg-white hover:border-blue-400 hover:bg-gray-50"
          }`}
        >
          <input {...getInputProps()} />
          <div className="flex flex-col items-center justify-center">
            <svg
              className="w-20 h-20 text-gray-400 mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
            <p className="text-2xl font-semibold text-gray-700 mb-2">
              {isDragActive ? "이미지를 여기에 놓으세요!" : "이미지 업로드"}
            </p>
            <p className="text-gray-500">
              클릭하거나 이미지를 드래그하세요 (JPG, PNG)
            </p>
            {uploadedFile && (
              <p className="mt-4 text-green-600 font-medium">
                업로드됨: {uploadedFile}
              </p>
            )}
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border-2 border-red-300 rounded-xl p-6 mb-8">
            <div className="flex items-start">
              <svg
                className="w-6 h-6 text-red-600 mr-3 flex-shrink-0 mt-0.5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-red-800 mb-1">오류</h3>
                <p className="text-red-700">{error}</p>
              </div>
              <button
                onClick={() => setError(null)}
                className="text-red-600 hover:text-red-800 ml-3"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">처리 중...</p>
          </div>
        )}

        {/* Matched Films */}
        {films.length > 0 && !loading && (
          <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
            <h2 className="text-3xl font-bold mb-6 text-gray-800">
              추천 필름 (Top 5)
            </h2>
            <div className="space-y-3 mb-6">
              {films.map((f, i) => (
                <div
                  key={i}
                  className="flex items-center justify-between p-4 bg-gradient-to-r from-gray-50 to-gray-100 rounded-lg hover:shadow-md transition-shadow"
                >
                  <div className="flex-1">
                    <div className="flex items-center mb-1">
                      <span className="inline-block w-8 h-8 bg-blue-600 text-white rounded-full text-center leading-8 font-bold mr-3">
                        {i + 1}
                      </span>
                      <span className="text-lg font-semibold text-gray-800">
                        {f.film_name}
                      </span>
                      <span className="ml-2 px-2 py-0.5 text-xs font-medium bg-blue-100 text-blue-700 rounded">
                        {f.tier.toUpperCase()}
                      </span>
                    </div>
                    <div className="ml-11 text-sm text-gray-600">
                      {f.manufacturer} | ISO {f.iso_base} | {f.type === 'color' ? '컬러' : '흑백'}
                    </div>
                    <div className="ml-11 text-xs text-gray-500 mt-1">
                      {f.reason}
                    </div>
                  </div>
                  <div className="text-right ml-4">
                    <span className="text-2xl font-bold text-blue-600">
                      {f.score}
                    </span>
                    <span className="text-gray-500 ml-1">점</span>
                  </div>
                </div>
              ))}
            </div>
            <button
              onClick={processImages}
              disabled={loading}
              className="w-full py-4 bg-gradient-to-r from-blue-600 to-blue-700 text-white text-lg font-semibold rounded-lg hover:from-blue-700 hover:to-blue-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-md hover:shadow-lg"
            >
              {loading ? "처리 중..." : "5개 필름 버전 생성하기"}
            </button>
          </div>
        )}

        {/* Results */}
        {results.length > 0 && (() => {
          const successResults = results.filter(r => r.status === 'success' && r.output_url);
          const failedResults = results.filter(r => r.status === 'failed');

          return (
            <>
              {/* ZIP Download (성공한 결과가 있을 때만) */}
              {successResults.length > 0 && (
                <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
                  <h2 className="text-3xl font-bold mb-6 text-gray-800">
                    처리 결과
                  </h2>
                  <a
                    href={`${API_BASE_URL.replace('/api', '')}/api/download/${jobId}/all_films.zip`}
                    download
                    className="block w-full py-4 bg-gradient-to-r from-green-600 to-green-700 text-white text-lg font-semibold rounded-lg hover:from-green-700 hover:to-green-800 transition-all text-center shadow-md hover:shadow-lg"
                  >
                    모든 필름 다운로드 (ZIP) - {successResults.length}개
                  </a>
                </div>
              )}

              {/* Failed Results Display */}
              {failedResults.length > 0 && (
                <div className="bg-yellow-50 border-2 border-yellow-300 rounded-xl p-6 mb-8">
                  <h3 className="text-lg font-semibold text-yellow-800 mb-3">
                    처리 실패한 필름 ({failedResults.length}개)
                  </h3>
                  <ul className="space-y-2">
                    {failedResults.map((r) => (
                      <li key={r.film_id} className="text-yellow-700">
                        • {r.film_name}: {r.error || '알 수 없는 오류'}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Success Results Grid */}
              {successResults.length > 0 && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {successResults.map((r) => (
                    <div
                      key={r.film_id}
                      className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-shadow"
                    >
                      <div className="relative aspect-video bg-gray-200">
                        <img
                          src={`${API_BASE_URL.replace('/api', '')}${r.output_url}`}
                          alt={r.film_name}
                          className="w-full h-full object-cover"
                          loading="lazy"
                          onError={(e) => {
                            (e.target as HTMLImageElement).src = '/placeholder-image.png';
                          }}
                        />
                      </div>
                      <div className="p-6">
                        <h3 className="text-xl font-bold mb-2 text-gray-800">
                          {r.film_name}
                        </h3>
                        {r.processing_time && (
                          <p className="text-sm text-gray-500 mb-3">
                            처리 시간: {r.processing_time}초
                          </p>
                        )}
                        <a
                          href={`${API_BASE_URL.replace('/api', '')}${r.output_url}`}
                          download
                          className="block w-full py-3 bg-blue-600 text-white text-center rounded-lg hover:bg-blue-700 transition-colors font-medium"
                        >
                          다운로드
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </>
          );
        })()}

        {/* Footer */}
        <div className="mt-16 text-center text-gray-500 text-sm">
          <p>Film Recipe v1.1.0 | Phase 2</p>
          <p className="mt-1">13 Professional Films (5 MVP + 8 Core) | Auto Film Matching by EXIF</p>
          <p className="mt-1 text-xs">Fujifilm | Kodak | Rollei</p>
        </div>
      </div>
    </main>
  );
}
