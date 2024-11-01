import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Video, Mic, Camera, StopCircle } from 'lucide-react';

const SeparateMediaRecorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordedVideo, setRecordedVideo] = useState(null);
  const [recordedAudio, setRecordedAudio] = useState(null);
  
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const videoRecorderRef = useRef(null);
  const audioRecorderRef = useRef(null);
  const videoChunksRef = useRef([]);
  const audioChunksRef = useRef([]);

  // 미디어 스트림 시작
  const startStream = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true
      });
      
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }

      // 비디오와 오디오 스트림 분리
      const videoStream = new MediaStream([stream.getVideoTracks()[0]]);
      const audioStream = new MediaStream([stream.getAudioTracks()[0]]);

      videoRecorderRef.current = new MediaRecorder(videoStream, {
        mimeType: 'video/webm;codecs=vp9'
      });

      audioRecorderRef.current = new MediaRecorder(audioStream, {
        mimeType: 'audio/webm;codecs=opus'
      });

      // 비디오 데이터 수집
      videoRecorderRef.current.ondataavailable = (e) => {
        if (e.data.size > 0) {
          videoChunksRef.current.push(e.data);
        }
      };

      // 오디오 데이터 수집
      audioRecorderRef.current.ondataavailable = (e) => {
        if (e.data.size > 0) {
          audioChunksRef.current.push(e.data);
        }
      };

      // 녹화가 중지되었을 때 처리
      videoRecorderRef.current.onstop = async () => {
        const videoBlob = new Blob(videoChunksRef.current, { type: 'video/webm' });
        await sendToServer(videoBlob, 'video', 'http://192.168.0.61:8000/v1/api/video-to-senti'); // 비디오 서버 전송
        setRecordedVideo(videoBlob);
      };

      audioRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        await sendToServer(audioBlob, 'audio', 'http://192.168.0.61:8000/v1/api/audio-to-text'); // 오디오 서버 전송POST
        setRecordedAudio(audioBlob);
      };

    } catch (error) {
      console.error('전송 중 오류 발생:', error.message);
      if (error.response) {
        console.error('서버 응답:', error.response.data);
        console.error('응답 상태:', error.response.status);
      } else if (error.request) {
        console.error('요청이 이루어졌으나 응답이 없음:', error.request);
      } else {
        console.error('Axios 설정 오류:', error.message);
      }
    }    
  };

  // 데이터 전송 함수
  const sendToServer = async (blob, type, url) => {
    const formData = new FormData();
    formData.append(type, blob, `recorded-${type}-${new Date().getTime()}.${type === 'video' ? 'webm' : 'webm'}`);

    try {
      const response = await axios.post(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      if (response.status !== 200) {
        throw new Error('네트워크 응답이 좋지 않습니다');
      }
      console.log(`${type} 데이터가 성공적으로 전송되었습니다.`);
    } catch (error) {
      console.error(`${type} 전송 중 오류 발생:`, error);
    }
  };

  // 녹화 시작
  const startRecording = () => {
    videoChunksRef.current = [];
    audioChunksRef.current = [];
    
    videoRecorderRef.current?.start();
    audioRecorderRef.current?.start();
    setIsRecording(true);
  };

  // 녹화 중지
  const stopRecording = () => {
    videoRecorderRef.current?.stop();
    audioRecorderRef.current?.stop();
    setIsRecording(false);
  };

  // 컴포넌트 마운트 시 스트림 시작
  useEffect(() => {
    startStream();
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  return (
    <div className="flex flex-col items-center gap-4 p-4">
      <div className="relative w-full max-w-2xl rounded-lg overflow-hidden bg-gray-100">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="w-full h-full"
        />
      </div>
      
      <div className="flex gap-4">
        {!isRecording ? (
          <button onClick={startRecording} className="flex items-center gap-2 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600">
            <Camera className="w-5 h-5" />
            녹화 시작
          </button>
        ) : (
          <button onClick={stopRecording} className="flex items-center gap-2 px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600">
            <StopCircle className="w-5 h-5" />
            녹화 중지
          </button>
        )}
        
        {recordedVideo && (
          <div> {/* 비디오 다운로드 버튼 및 기타 요소들 */} </div>
        )}
        
        {recordedAudio && (
          <div> {/* 오디오 다운로드 버튼 및 기타 요소들 */} </div>
        )}
      </div>

      {/* 녹화된 비디오 및 오디오 재생 */}
      {recordedVideo && (
        <div className="w-full max-w-2xl mt-4">
          <h3 className="text-lg font-semibold mb-2">녹화된 비디오:</h3>
          <video controls src={URL.createObjectURL(recordedVideo)} className="w-full rounded-lg" />
        </div>
      )}

      {recordedAudio && (
        <div className="w-full max-w-2xl mt-4">
          <h3 className="text-lg font-semibold mb-2">녹화된 오디오:</h3>
          <audio controls src={URL.createObjectURL(recordedAudio)} className="w-full" />
        </div>
      )}
    </div>
  );
};

export default SeparateMediaRecorder;
