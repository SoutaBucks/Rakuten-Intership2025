"use client"

import React, { useState, useEffect } from 'react';
import { MapPin, AlertTriangle, Phone, Droplets, Shield} from "lucide-react"
import styles from './Info.module.css';
import { Link } from 'react-router-dom';

// Button component remains unchanged
function Button({ children, className = "", variant = "default", ...props }) {
  const variantClasses = {
    default: styles.btnDefault,
    destructive: styles.btnDestructive,
    secondary: styles.btnSecondary,
  };
  return (
    <button className={`${styles.btn} ${variantClasses[variant]} ${className}`} {...props}>
      {children}
    </button>
  );
}

export default function Info() {
  const [emergencyInfo, setEmergencyInfo] = useState({
    embassy: null,
    jpEmergency: [],
    loading: true,
    error: null,
  });

  useEffect(() => {
    // ▼▼▼ここから変更点▼▼▼

    // 1. localStorageからキャッシュされた予約情報を取得
    const cachedData = localStorage.getItem("reservationResult");

    // 2. キャッシュが存在すれば、そのデータを直接stateにセットする
    if (cachedData) {
      console.log("✅ キャッシュからデータを読み込みます。APIリクエストは行いません。");
      try {
        const reservationResult = JSON.parse(cachedData);
        
        // stateをキャッシュデータで更新
        setEmergencyInfo({
          embassy: reservationResult.embassies?.[0] || null,
          jpEmergency: reservationResult.jp_emergency || [],
          loading: false, // データ読み込み完了
          error: null,
        });

      } catch (e) {
        console.error("キャッシュデータの解析に失敗しました:", e);
        // エラーが発生した場合は、フォールバックとしてAPIを呼び出すことも可能
        setEmergencyInfo({ embassy: null, jpEmergency: [], loading: false, error: "Failed to parse cached data." });
      }

    } else {
      // 3. キャッシュがない場合のみ、フォールバックとしてAPIにリクエストを送信
      console.log("⚠️ キャッシュがありません。APIにリクエストを送信します。");

      const fetchEmergencyContacts = async () => {
        try {
          const response = await fetch('http://127.0.0.1:8000/api/embassy/near', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              address: "2-8-1 Nishi-Shinjuku, Shinjuku-ku, Tokyo", // デフォルトの住所
              nationality: "United States", // デフォルトの国籍
              limit: 3
            }),
          });

          if (!response.ok) throw new Error(`API Error: ${response.status}`);
          const data = await response.json();
          setEmergencyInfo({
            embassy: data.embassies?.[0] || null,
            jpEmergency: data.jp_emergency || [],
            loading: false,
            error: null,
          });
        } catch (err) {
          console.error("Failed to fetch emergency contacts:", err);
          setEmergencyInfo({
            embassy: null,
            jpEmergency: [],
            loading: false,
            error: "Failed to retrieve contact information.",
          });
        }
      };
      
      fetchEmergencyContacts();
    }
    }, []);


  return (
    <div className={styles.pageContainer}>
      <div className={styles.contentWrapper}>
        {/* Header */}
        <header className={styles.header}>
          <div className={styles.headerTitleGroup}>
            <Shield className={styles.headerIcon} />
            <h1 className={styles.headerTitle}>
              Emergency Information System
            </h1>
          </div>
          <p className={styles.headerSubtitle}>
            Access critical information during a disaster
          </p>
        </header>

        {/* Main Content Cards */}
        <div className={styles.cardsGrid}>
          {/* Evacuation Shelters */}
          <div className={styles.card}>
            <div className={styles.cardHeader}>
              <MapPin className={styles.cardIcon} />
              <h2 className={styles.cardTitle}>Evacuation Shelter Map</h2>
            </div>
            <p className={styles.cardText}>
              View the locations of nearby evacuation shelters on the map.
            </p>
            <Link to="/shelter">
              <Button className={styles.fullWidthButton}>
                <MapPin className={styles.cardButtonIcon} />
                Open Map
              </Button>
            </Link>
          </div>

          {/* Flood Areas */}
          <div className={styles.card}>
            <div className={styles.cardHeader}>
              <Droplets className={styles.cardIcon} />
              <h2 className={styles.cardTitle}>Flood Zone Map</h2>
            </div>
            <p className={styles.cardText}>
              Displays anticipated flood zones and risk levels.
            </p>
            <Link to="/flooding">
              <Button className={styles.fullWidthButton}>
                <Droplets className={styles.cardButtonIcon} />
                Open Flood Map
              </Button>
            </Link>
          </div>

          {/* Emergency Contacts */}
          <div className={`${styles.card} ${styles.colSpan2}`}>
            <div className={styles.cardHeader}>
              <Phone className={styles.cardIcon} />
              <h2 className={styles.cardTitle}>Emergency Contacts</h2>
            </div>
            <p className={styles.cardText}>
              A list of contacts for embassies and emergency services.
            </p>
            <div className={styles.contactsList}>
              {emergencyInfo.loading && <p>Loading contacts...</p>}
              {emergencyInfo.error && <p className={styles.textDestructive}>{emergencyInfo.error}</p>}
              
              {!emergencyInfo.loading && !emergencyInfo.error && (
                <>
                  {emergencyInfo.embassy && (
                    <div className={`${styles.contactItem} ${styles.contactItemHighlight}`}>
                      {/* NOTE: The API currently returns Japanese names. `name_en` would be ideal. */}
                      <span className={styles.contactLabel}>{emergencyInfo.embassy.name_ja}</span>
                      <a href={`tel:${emergencyInfo.embassy.phone}`} className={`${styles.contactNumber} ${styles.contactNumberEmbassy}`}>
                        {emergencyInfo.embassy.phone}
                      </a>
                    </div>
                  )}

                  {emergencyInfo.jpEmergency.map(contact => (
                       <div className={styles.contactItem} key={contact.number}>
                          {/* NOTE: The API currently returns Japanese descriptions. `desc_en` would be ideal. */}
                          <span className={styles.contactLabel}>{contact.desc_ja}</span>
                          <span className={styles.contactNumber}>{contact.number}</span>
                       </div>
                  ))}
                  
                  <div className={styles.contactItem}>
                    <span className={styles.contactLabel}>Disaster Message Dial</span>
                    <span className={styles.contactNumber}>171</span>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>

        
        {/* Emergency Guidelines */}
        <div className={styles.card}>
          <div className={styles.guidelinesHeader}>
            <AlertTriangle className={styles.guidelinesIcon} />
            <h2 className={styles.guidelinesTitle}>Emergency Guidelines</h2>
          </div>
          <div className={styles.guidelinesGrid}>
            <div>
              {[
                "Stay calm and protect your head. Move away from windows or heavy objects.",
                "Follow instructions from hotel staff and local authorities. Look for evacuation signs.",
                "Use hotel or public Wi-Fi to contact your family and embassy to report your safety.",
              ].map((text, index) => (
                <div key={index} className={styles.guidelineItem}>
                  <div className={styles.guidelineNumber}>{index + 1}</div>
                  <p className={styles.guidelineText}>{text}</p>
                </div>
              ))}
            </div>
            <div>
              {[
                "Get official information from TV, radio, or hotel staff. Be careful with social media rumors.",
                "Keep your passport, phone, and wallet with you if you need to evacuate.",
                "For immediate danger, call 119 (Fire/Ambulance) or 110 (Police).",
              ].map((text, index) => (
                <div key={index} className={styles.guidelineItem}>
                  <div className={styles.guidelineNumber}>{index + 4}</div>
                  <p className={styles.guidelineText}>{text}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        {/* Footer */}
        <footer className={styles.footer}>
          <div className={styles.footerUpdateInfo}>
            <span className={styles.footerText}>© Rakuten Group, Inc.</span>
          </div>
        </footer>
        
      </div>
    </div>
  );
}