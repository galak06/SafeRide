import React, { useState, useRef, useEffect } from 'react'
import { useLanguage } from '../contexts/LanguageContext'
import './LanguageSelector.css'

interface LanguageSelectorProps {
  className?: string
  showLabel?: boolean
}

const LanguageSelector: React.FC<LanguageSelectorProps> = ({ 
  className = '', 
  showLabel = true 
}) => {
  const { language, setLanguage, t, languages } = useLanguage()
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [])

  const handleLanguageSelect = (lang: keyof typeof languages) => {
    setLanguage(lang)
    setIsOpen(false)
  }

  const currentLanguage = languages[language]

  return (
    <div className={`language-selector ${className}`} ref={dropdownRef}>
      {showLabel && (
        <label className="language-label">
          {t('languageSelector.title')}
        </label>
      )}
      
      <div className="language-dropdown">
        <button
          className="language-button"
          onClick={() => setIsOpen(!isOpen)}
          aria-label={t('languageSelector.selectLanguage')}
        >
          <span className="language-flag">{currentLanguage.flag}</span>
          <span className="language-name">{currentLanguage.name}</span>
          <span className={`dropdown-arrow ${isOpen ? 'open' : ''}`}>▼</span>
        </button>

        {isOpen && (
          <div className="language-options">
            {Object.entries(languages).map(([code, lang]) => (
              <button
                key={code}
                className={`language-option ${code === language ? 'active' : ''}`}
                onClick={() => handleLanguageSelect(code as keyof typeof languages)}
                aria-label={`Select ${lang.name}`}
              >
                <span className="language-flag">{lang.flag}</span>
                <span className="language-name">{lang.name}</span>
                {code === language && <span className="checkmark">✓</span>}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default LanguageSelector 