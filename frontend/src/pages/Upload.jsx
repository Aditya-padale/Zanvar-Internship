// src/pages/Upload.jsx
import React, { useState } from "react";
import { uploadFile } from '../api';

const Upload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState("");

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setUploadProgress(0);
      setStatus("");
      setUploading(true);
      try {
        // Use fetch-based uploadFile utility
        const res = await uploadFile(file);
        if (res.error) {
          setStatus(`Upload failed: ${res.error}`);
        } else {
          setUploadProgress(100);
          setStatus("Processing...");
          // Save uploaded file info to localStorage for Chat page
          localStorage.setItem('uploadedFile', JSON.stringify({
            filename: res.filename,
            format: res.filename.split('.').pop().toUpperCase()
          }));
          setTimeout(() => {
            window.location.href = '/chat';
          }, 1000);
        }
      } catch (err) {
        setStatus("Upload failed: " + err.message);
      } finally {
        setUploading(false);
      }
    }
  };

  return (
    <div className="relative flex size-full min-h-screen flex-col bg-[#141a1f] dark group/design-root overflow-x-hidden" style={{ fontFamily: 'Inter, "Noto Sans", sans-serif' }}>
      <div className="layout-container flex h-full grow flex-col">
        {/* Header */}
        <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-b-[#2b3640] px-10 py-3">
          <div className="flex items-center gap-4 text-white">
            <div className="size-4">
              {/* Logo SVG */}
              <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path fillRule="evenodd" clipRule="evenodd" d="M24 18.4228L42 11.475V34.3663C42 34.7796 41.7457 35.1504 41.3601 35.2992L24 42V18.4228Z" fill="currentColor"></path>
                <path fillRule="evenodd" clipRule="evenodd" d="M24 8.18819L33.4123 11.574L24 15.2071L14.5877 11.574L24 8.18819ZM9 15.8487L21 20.4805V37.6263L9 32.9945V15.8487ZM27 37.6263V20.4805L39 15.8487V32.9945L27 37.6263ZM25.354 2.29885C24.4788 1.98402 23.5212 1.98402 22.646 2.29885L4.98454 8.65208C3.7939 9.08038 3 10.2097 3 11.475V34.3663C3 36.0196 4.01719 37.5026 5.55962 38.098L22.9197 44.7987C23.6149 45.0671 24.3851 45.0671 25.0803 44.7987L42.4404 38.098C43.9828 37.5026 45 36.0196 45 34.3663V11.475C45 10.2097 44.2061 9.08038 43.0155 8.65208L25.354 2.29885Z" fill="currentColor"></path>
              </svg>
            </div>
            <h2 className="text-white text-lg font-bold leading-tight tracking-[-0.015em]">Zanvar Data Insights</h2>
          </div>
          <div className="flex flex-1 justify-end gap-8">
            <div className="flex items-center gap-9">
              <a className="text-white text-sm font-medium leading-normal" href="#">Home</a>
              <a className="text-white text-sm font-medium leading-normal" href="#">Features</a>
              <a className="text-white text-sm font-medium leading-normal" href="#">Pricing</a>
              <a className="text-white text-sm font-medium leading-normal" href="#">Support</a>
            </div>
            <div className="flex gap-2 items-center">
              <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-4 bg-[#dce8f3] text-[#141a1f] text-sm font-bold leading-normal tracking-[0.015em]">
                <span className="truncate">Get Started</span>
              </button>
              <div
                className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10 cursor-pointer border-2 border-[#dce8f3] hover:border-[#4fd1c5] transition-colors"
                style={{ backgroundImage: `url('https://lh3.googleusercontent.com/aida-public/AB6AXuDYdyNgyyZJ4noBYbSowbQlmHmOoT39UUwlEC_T057UfEahdu0OnGFRFCxmREtADsrlfZR9KE8G8w0As4FIHwcpS0lJf4WTu3Z8h-g4OzroeQn7u_R18GyuHYiqffgV_Ego8eJ3ON9Z2cBdt1YRrHSWUWkh2_hFmrUczIs6zmWo5sKsTOXmroNtBKycJ3CTJ5_s8KzaCsq7iH00lmHZGqhl9HGn6fEQFRYjBUwGdGifsFqPzptMAhVi4O5TPHtzdIhvYg7XI9esHsA')` }}
                onClick={() => window.location.href = '/profile'}
                title="Go to Profile"
              ></div>
            </div>
          </div>
        </header>
        {/* Upload Section */}
        <div className="px-40 flex flex-1 justify-center py-5">
          <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
            <div className="flex flex-wrap justify-between gap-3 p-4">
              <p className="text-white tracking-light text-[32px] font-bold leading-tight min-w-72">Upload Your Excel File</p>
            </div>
            <div className="flex flex-col p-4">
              <div className="flex flex-col items-center gap-6 rounded-xl border-2 border-dashed border-[#3d4d5c] px-6 py-14">
                <div className="flex max-w-[480px] flex-col items-center gap-2">
                  <p className="text-white text-lg font-bold leading-tight tracking-[-0.015em] max-w-[480px] text-center">Drag and drop your file here, or</p>
                  <p className="text-white text-sm font-normal leading-normal max-w-[480px] text-center">We support .xlsx and .csv files</p>
                </div>
                {/* Browse Files Button and Hidden Input */}
                <input
                  type="file"
                  id="file-upload"
                  accept=".xlsx,.csv"
                  className="hidden"
                  onChange={handleFileChange}
                />
                <button
                  className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-4 bg-[#2b3640] text-white text-sm font-bold leading-normal tracking-[0.015em]"
                  onClick={() => document.getElementById('file-upload').click()}
                  type="button"
                >
                  <span className="truncate">Browse Files</span>
                </button>
                {selectedFile && (
                  <p className="text-[#9daebe] text-sm font-normal leading-normal pt-2">Selected file: {selectedFile.name}</p>
                )}
              </div>
            </div>
            {/* Upload Progress Section */}
            {selectedFile && (
              <div className="flex flex-col gap-3 p-4">
                <div className="flex gap-6 justify-between">
                  <p className="text-white text-base font-medium leading-normal">
                    {uploading ? "Uploading..." : status ? status : "Upload complete!"}
                  </p>
                </div>
                <div className="rounded bg-[#3d4d5c]">
                  <div
                    className="h-2 rounded bg-[#dce8f3] transition-all duration-500"
                    style={{ width: `${uploadProgress}%` }}
                  ></div>
                </div>
                <p className="text-[#9daebe] text-sm font-normal leading-normal">{uploadProgress}%</p>
              </div>
            )}
            {selectedFile && (
              <p className="text-[#9daebe] text-sm font-normal leading-normal pb-3 pt-1 px-4 text-center">File: {selectedFile.name}</p>
            )}
            {status && (
              <p className="text-[#9daebe] text-sm font-normal leading-normal pb-3 pt-1 px-4 text-center">Status: {status}</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Upload;
