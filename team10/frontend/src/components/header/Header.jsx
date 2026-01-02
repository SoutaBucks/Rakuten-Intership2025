import React from "react";
import "./Header.css";

export default function Header() {
  return (
    <div className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-8">
            <img src="/assets/travel2.png" alt="" className="logoImg" />
            <p className="title">Thanks for visiting our site!</p>
            <hr className="headerBorder" />
            {/* <nav className="hidden md:flex space-x-6">
              <a href="#" className="text-gray-700 hover:text-red-600">
                国内宿泊
              </a>
              <a href="#" className="text-gray-700 hover:text-red-600">
                海外ホテル
              </a>
              <a href="#" className="text-gray-700 hover:text-red-600">
                航空券
              </a>
              <a href="#" className="text-gray-700 hover:text-red-600">
                レンタカー
              </a>
              <a href="#" className="text-gray-700 hover:text-red-600">
                高速バス
              </a>
            </nav> */}
          </div>
          {/* <div className="flex items-center space-x-4">
            <button variant="outline" size="sm">
              ログイン
            </button>
            <button size="sm" className="bg-red-600 hover:bg-red-700">
              新規登録
            </button>
          </div> */}
        </div>
      </div>
    </div>
  );
}
