import React, { useState } from "react";

const PROFILE_AVATAR = "https://lh3.googleusercontent.com/aida-public/AB6AXuDYdyNgyyZJ4noBYbSowbQlmHmOoT39UUwlEC_T057UfEahdu0OnGFRFCxmREtADsrlfZR9KE8G8w0As4FIHwcpS0lJf4WTu3Z8h-g4OzroeQn7u_R18GyuHYiqffgV_Ego8eJ3ON9Z2cBdt1YRrHSWUWkh2_hFmrUczIs6zmWo5sKsTOXmroNtBKycJ3CTJ5_s8KzaCsq7iH00lmHZGqhl9HGn6fEQFRYjBUwGdGifsFqPzptMAhVi4O5TPHtzdIhvYg7XI9esHsA";

const Profile = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // Add logic to update profile info or password
    alert("Profile updated (demo only)");
  };

  return (
    <div className="relative flex size-full min-h-screen flex-col bg-[#141a1f] dark group/design-root overflow-x-hidden" style={{ fontFamily: 'Inter, "Noto Sans", sans-serif' }}>
      <div className="layout-container flex h-full grow flex-col">
        <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-b-[#2b3640] px-10 py-3">
          <div className="flex items-center gap-4 text-white">
            <div className="size-4">
              <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M36.7273 44C33.9891 44 31.6043 39.8386 30.3636 33.69C29.123 39.8386 26.7382 44 24 44C21.2618 44 18.877 39.8386 17.6364 33.69C16.3957 39.8386 14.0109 44 11.2727 44C7.25611 44 4 35.0457 4 24C4 12.9543 7.25611 4 11.2727 4C14.0109 4 16.3957 8.16144 17.6364 14.31C18.877 8.16144 21.2618 4 24 4C26.7382 4 29.123 8.16144 30.3636 14.31C31.6043 8.16144 33.9891 4 36.7273 4C40.7439 4 44 12.9543 44 24C44 35.0457 40.7439 44 36.7273 44Z" fill="currentColor"></path>
              </svg>
            </div>
            <h2 className="text-white text-lg font-bold leading-tight tracking-[-0.015em]">Zanvar</h2>
          </div>
          <div className="flex flex-1 justify-end gap-8">
            <div
              className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10 cursor-pointer border-2 border-[#dce8f3] hover:border-[#4fd1c5] transition-colors"
              style={{ backgroundImage: `url('${PROFILE_AVATAR}')` }}
              onClick={() => window.location.href = '/profile'}
              title="Go to Profile"
            ></div>
          </div>
        </header>
        <div className="px-40 flex flex-1 justify-center py-5">
          <form className="layout-content-container flex flex-col max-w-[960px] flex-1" onSubmit={handleSubmit}>
            <div className="flex flex-wrap justify-between gap-3 p-4">
              <p className="text-white tracking-light text-[32px] font-bold leading-tight min-w-72">Account Settings</p>
            </div>
            <h3 className="text-white text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">Profile Information</h3>
            <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
              <label className="flex flex-col min-w-40 flex-1">
                <p className="text-white text-base font-medium leading-normal pb-2">Name</p>
                <input
                  className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-white focus:outline-0 focus:ring-0 border border-[#3d4d5c] bg-[#1f272e] focus:border-[#3d4d5c] h-14 placeholder:text-[#9daebe] p-[15px] text-base font-normal leading-normal"
                  value={name}
                  onChange={e => setName(e.target.value)}
                  placeholder="Enter your name"
                />
              </label>
            </div>
            <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
              <label className="flex flex-col min-w-40 flex-1">
                <p className="text-white text-base font-medium leading-normal pb-2">Email</p>
                <input
                  className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-white focus:outline-0 focus:ring-0 border border-[#3d4d5c] bg-[#1f272e] focus:border-[#3d4d5c] h-14 placeholder:text-[#9daebe] p-[15px] text-base font-normal leading-normal"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  placeholder="Enter your email"
                />
              </label>
            </div>
            <h3 className="text-white text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">Security</h3>
            <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
              <label className="flex flex-col min-w-40 flex-1">
                <p className="text-white text-base font-medium leading-normal pb-2">Current Password</p>
                <input
                  type="password"
                  className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-white focus:outline-0 focus:ring-0 border border-[#3d4d5c] bg-[#1f272e] focus:border-[#3d4d5c] h-14 placeholder:text-[#9daebe] p-[15px] text-base font-normal leading-normal"
                  value={currentPassword}
                  onChange={e => setCurrentPassword(e.target.value)}
                  placeholder="Enter current password"
                />
              </label>
            </div>
            <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
              <label className="flex flex-col min-w-40 flex-1">
                <p className="text-white text-base font-medium leading-normal pb-2">New Password</p>
                <input
                  type="password"
                  placeholder="Enter new password"
                  className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-white focus:outline-0 focus:ring-0 border border-[#3d4d5c] bg-[#1f272e] focus:border-[#3d4d5c] h-14 placeholder:text-[#9daebe] p-[15px] text-base font-normal leading-normal"
                  value={newPassword}
                  onChange={e => setNewPassword(e.target.value)}
                />
              </label>
            </div>
            <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
              <label className="flex flex-col min-w-40 flex-1">
                <p className="text-white text-base font-medium leading-normal pb-2">Confirm New Password</p>
                <input
                  type="password"
                  placeholder="Confirm new password"
                  className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-white focus:outline-0 focus:ring-0 border border-[#3d4d5c] bg-[#1f272e] focus:border-[#3d4d5c] h-14 placeholder:text-[#9daebe] p-[15px] text-base font-normal leading-normal"
                  value={confirmPassword}
                  onChange={e => setConfirmPassword(e.target.value)}
                />
              </label>
            </div>
            <div className="flex px-4 py-3 justify-end">
              <button
                className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-xl h-10 px-4 bg-[#dce8f3] text-[#141a1f] text-sm font-bold leading-normal tracking-[0.015em]"
                type="submit"
              >
                <span className="truncate">Update Settings</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Profile;
