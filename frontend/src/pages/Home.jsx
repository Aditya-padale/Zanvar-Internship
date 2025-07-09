// src/pages/Home.jsx
import React from "react";

const Home = () => {
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
              <a className="text-white text-sm font-medium leading-normal" href="#">Product</a>
              <a className="text-white text-sm font-medium leading-normal" href="#">Solutions</a>
              <a className="text-white text-sm font-medium leading-normal" href="#">Pricing</a>
              <a className="text-white text-sm font-medium leading-normal" href="#">Resources</a>
            </div>
            <div className="flex gap-2 items-center">
              <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-4 bg-[#dce8f3] text-[#141a1f] text-sm font-bold leading-normal tracking-[0.015em]">
                <span className="truncate">Get started</span>
              </button>
              <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-4 bg-[#2b3640] text-white text-sm font-bold leading-normal tracking-[0.015em]">
                <span className="truncate">Log in</span>
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
        {/* Hero Section */}
        <div className="px-40 flex flex-1 justify-center py-5">
          <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
            <div>
              <div>
                <div
                  className="flex min-h-[480px] flex-col gap-6 bg-cover bg-center bg-no-repeat items-center justify-center p-4 rounded-xl"
                  style={{backgroundImage: 'linear-gradient(rgba(0, 0, 0, 0.1) 0%, rgba(0, 0, 0, 0.4) 100%), url("https://lh3.googleusercontent.com/aida-public/AB6AXuDUmxnffFeWUiFgPt73bdSsOiBGMEl2_8RBwoc6EfPDEb11L8mMqIK3Lxcx58fuNMX_0seBOIkMpghLVk1yhGp9uIgcsM_MiV1NVGqw3zlyHsXgRnP63k2iazwSBvdxj6q8yK0FA2GmIvLhdlTCS3srrp97_hCFaYl_Ql9xhxnsokHIR-Qc9H6mqubKwJvgtT05u2ERrdOUK50m9jHUO7sh7pr-KSC8nvucPBi4U_Cji3cR6QAfsi-3HRLevEI8ogtuZtjAADYFP3g")'}}
                >
                  <div className="flex flex-col gap-2 text-center">
                    <h1 className="text-white text-4xl font-black leading-tight tracking-[-0.033em]">Unlock the Power of Your Data with AI</h1>
                    <h2 className="text-white text-sm font-normal leading-normal">Transform your spreadsheets into actionable insights with our AI-powered chatbot. Analyze, visualize, and understand your data like never before.</h2>
                  </div>
                  <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-4 bg-[#dce8f3] text-[#141a1f] text-sm font-bold leading-normal tracking-[0.015em] mt-4"
                  onClick={() => window.location.href = '/upload'}
                  >
                    <span className="truncate">Upload Your File</span>
                  </button>
                </div>
              </div>
            </div>
            {/* Features Section */}
            <div className="flex flex-col gap-10 px-4 py-10">
              <div className="flex flex-col gap-4">
                <h1 className="text-white tracking-light text-[32px] font-bold leading-tight max-w-[720px]">Key Features</h1>
                <p className="text-white text-base font-normal leading-normal max-w-[720px]">Explore the capabilities that make data analysis effortless and insightful.</p>
              </div>
              <div className="grid grid-cols-[repeat(auto-fit,minmax(158px,1fr))] gap-3 p-0">
                {/* Feature 1 */}
                <div className="flex flex-1 gap-3 rounded-lg border border-[#3d4d5c] bg-[#1f272e] p-4 flex-col">
                  <div className="text-white">
                    {/* Magic Wand SVG */}
                    <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
                      <path d="M48,64a8,8,0,0,1,8-8H72V40a8,8,0,0,1,16,0V56h16a8,8,0,0,1,0,16H88V88a8,8,0,0,1-16,0V72H56A8,8,0,0,1,48,64ZM184,192h-8v-8a8,8,0,0,0-16,0v8h-8a8,8,0,0,0,0,16h8v8a8,8,0,0,0,16,0v-8h8a8,8,0,0,0,0-16Zm56-48H224V128a8,8,0,0,0-16,0v16H192a8,8,0,0,0,0,16h16v16a8,8,0,0,0,16,0V160h16a8,8,0,0,0,0-16ZM219.31,80,80,219.31a16,16,0,0,1-22.62,0L36.68,198.63a16,16,0,0,1,0-22.63L176,36.69a16,16,0,0,1,22.63,0l20.68,20.68A16,16,0,0,1,219.31,80Zm-54.63,32L144,91.31l-96,96L68.68,208ZM208,68.69,187.31,48l-32,32L176,100.69Z"></path>
                    </svg>
                  </div>
                  <div className="flex flex-col gap-1">
                    <h2 className="text-white text-base font-bold leading-tight">AI-Powered Insights</h2>
                    <p className="text-[#9daebe] text-sm font-normal leading-normal">Leverage advanced AI algorithms to uncover hidden patterns and trends in your data.</p>
                  </div>
                </div>
                {/* Feature 2 */}
                <div className="flex flex-1 gap-3 rounded-lg border border-[#3d4d5c] bg-[#1f272e] p-4 flex-col">
                  <div className="text-white">
                    {/* Chatbot SVG */}
                    <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
                      <path d="M140,128a12,12,0,1,1-12-12A12,12,0,0,1,140,128ZM84,116a12,12,0,1,0,12,12A12,12,0,0,0,84,116Zm88,0a12,12,0,1,0,12,12A12,12,0,0,0,172,116Zm60,12A104,104,0,0,1,79.12,219.82L45.07,231.17a16,16,0,0,1-20.24-20.24l11.35-34.05A104,104,0,1,1,232,128Zm-16,0A88,88,0,1,0,51.81,172.06a8,8,0,0,1,.66,6.54L40,216,77.4,203.53a7.85,7.85,0,0,1,2.53-.42,8,8,0,0,1,4,1.08A88,88,0,0,0,216,128Z"></path>
                    </svg>
                  </div>
                  <div className="flex flex-col gap-1">
                    <h2 className="text-white text-base font-bold leading-tight">Chatbot Interface</h2>
                    <p className="text-[#9daebe] text-sm font-normal leading-normal">Interact with your data through a conversational chatbot, asking questions and receiving instant answers.</p>
                  </div>
                </div>
                {/* Feature 3 */}
                <div className="flex flex-1 gap-3 rounded-lg border border-[#3d4d5c] bg-[#1f272e] p-4 flex-col">
                  <div className="text-white">
                    {/* Chart SVG */}
                    <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
                      <path d="M216,40H136V24a8,8,0,0,0-16,0V40H40A16,16,0,0,0,24,56V176a16,16,0,0,0,16,16H79.36L57.75,219a8,8,0,0,0,12.5,10l29.59-37h56.32l29.59,37a8,8,0,1,0,12.5-10l-21.61-27H216a16,16,0,0,0,16-16V56A16,16,0,0,0,216,40Zm0,136H40V56H216V176ZM104,120v24a8,8,0,0,1-16,0V120a8,8,0,0,1,16,0Zm32-16v40a8,8,0,0,1-16,0V104a8,8,0,0,1,16,0Zm32-16v56a8,8,0,0,1-16,0V88a8,8,0,0,1,16,0Z"></path>
                    </svg>
                  </div>
                  <div className="flex flex-col gap-1">
                    <h2 className="text-white text-base font-bold leading-tight">Data Visualization</h2>
                    <p className="text-[#9daebe] text-sm font-normal leading-normal">Generate interactive charts and graphs to visualize your data and communicate findings effectively.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        {/* Footer */}
        <footer className="flex justify-center">
          <div className="flex max-w-[960px] flex-1 flex-col">
            <footer className="flex flex-col gap-6 px-5 py-10 text-center">
              <div className="flex flex-wrap items-center justify-center gap-6">
                <a className="text-[#9daebe] text-base font-normal leading-normal min-w-40" href="#">Product</a>
                <a className="text-[#9daebe] text-base font-normal leading-normal min-w-40" href="#">Solutions</a>
                <a className="text-[#9daebe] text-base font-normal leading-normal min-w-40" href="#">Pricing</a>
                <a className="text-[#9daebe] text-base font-normal leading-normal min-w-40" href="#">Resources</a>
                <a className="text-[#9daebe] text-base font-normal leading-normal min-w-40" href="#">Contact Us</a>
              </div>
              <p className="text-[#9daebe] text-base font-normal leading-normal">© 2024 Zanvar Data Insights. All rights reserved.</p>
            </footer>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default Home;
