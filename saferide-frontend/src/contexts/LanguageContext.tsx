import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react'

// Supported languages
export type Language = 'en' | 'he'

// Language configuration
const LANGUAGES = {
  en: {
    name: 'English',
    flag: '🇺🇸',
    direction: 'ltr' as const
  },
  he: {
    name: 'עברית',
    flag: '🇮🇱',
    direction: 'rtl' as const
  }
} as const

// Translation files
import enTranslations from '../locales/en.json'
import heTranslations from '../locales/he.json'

const translations: Record<Language, any> = {
  en: enTranslations,
  he: heTranslations
}

// Language context interface
interface LanguageContextType {
  language: Language
  setLanguage: (lang: Language) => void
  t: (key: string) => string
  direction: 'ltr' | 'rtl'
  languages: typeof LANGUAGES
}

// Create context
const LanguageContext = createContext<LanguageContextType | undefined>(undefined)

// Language provider props
interface LanguageProviderProps {
  children: ReactNode
}

// Language provider component
export const LanguageProvider: React.FC<LanguageProviderProps> = ({ children }) => {
  const [language, setLanguageState] = useState<Language>('en')

  // Set language and update document direction
  const setLanguage = (lang: Language) => {
    setLanguageState(lang)
    localStorage.setItem('preferredLanguage', lang)
    
    // Update document direction for RTL support
    document.documentElement.dir = LANGUAGES[lang].direction
    document.documentElement.lang = lang
  }

  // Translation function
  const t = (key: string): string => {
    const keys = key.split('.')
    let value: any = translations[language]
    
    for (const k of keys) {
      if (value && typeof value === 'object' && k in value) {
        value = value[k]
      } else {
        // Fallback to English if translation not found
        value = keys.reduce((obj, k) => obj?.[k], translations.en) || key
        break
      }
    }
    
    return typeof value === 'string' ? value : key
  }

  // Initialize language on mount
  useEffect(() => {
    const savedLanguage = localStorage.getItem('preferredLanguage') as Language
    const browserLanguage = navigator.language.split('-')[0] as string
    
    // Set language priority: saved > browser > default (English)
    const initialLanguage = savedLanguage || 
                          (browserLanguage in LANGUAGES ? browserLanguage as Language : 'en')
    
    setLanguage(initialLanguage)
  }, [])

  const contextValue: LanguageContextType = {
    language,
    setLanguage,
    t,
    direction: LANGUAGES[language].direction,
    languages: LANGUAGES
  }

  return (
    <LanguageContext.Provider value={contextValue}>
      {children}
    </LanguageContext.Provider>
  )
}

// Hook to use language context
export const useLanguage = (): LanguageContextType => {
  const context = useContext(LanguageContext)
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider')
  }
  return context
} 