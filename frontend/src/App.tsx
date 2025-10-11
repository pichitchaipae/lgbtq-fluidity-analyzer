import { useMutation } from "@tanstack/react-query";
import { useState } from "react";

import { analyzeSurvey } from "./api";
import type { AnalysisResponse, SurveyAnswers } from "./types";

type Language = "th" | "en";

const initialAnswers: SurveyAnswers = {
  media1: 0,
  media2: 0,
  family1: 0,
  family2: 0,
  family3: 0,
  community1: 0,
  community2: 0,
  culture1: 0,
  culture2: 0,
  exploration1: 0,
  exploration2: 0,
  school1: 0,
};

const Option = ({ value, label }: { value: number; label: string }) => (
  <option value={value}>{label}</option>
);

const translations = {
  th: {
    title: "เครื่องมือวิเคราะห์ความหลากหลายทางเพศ LGBTQ+",
    subtitle: "เครื่องมือเพื่อการศึกษาและการวิจัยที่ช่วยให้คุณทำความเข้าใจมิติของความหลากหลายทางเพศ โดยไม่จัดเก็บข้อมูลส่วนบุคคล พัฒนาตามมาตรฐานจริยธรรมการวิจัยและความเป็นส่วนตัว",
    badge1: "🔒 ไม่เก็บข้อมูล",
    badge2: "🧠 เชิงสถิติ",
    badge3: "🎓 เพื่อการศึกษา",
    badge4: "🌍 SDG 3, 5, 10",
    surveyTitle: "แบบสอบถาม",
    surveyDesc: "กรอกข้อมูลเพื่อวิเคราะห์แนวโน้ม",
    resultTitle: "ผลการวิเคราะห์",
    resultDesc: "Summary",
    resetBtn: "🔄 ล้างข้อมูล",
    submitBtn: "✨ คำนวณผลลัพธ์",
    submittingBtn: "⏳ กำลังคำนวณ...",
    errorMsg: "❌ เกิดข้อผิดพลาดในการประมวลผล กรุณาลองใหม่อีกครั้ง",
    successMsg: "✅ ประมวลผลสำเร็จ",
    scoreRange: "ช่วงคะแนน",
    processedAt: "ประมวลผลเมื่อ",
    points: "คะแนน",
    noteTitle: "⚠️ หมายเหตุ",
    refsTitle: "📚 เอกสารอ้างอิง",
    disclaimer: "ผลลัพธ์นี้เป็นแนวโน้มเชิงสถิติจากการตอบแบบสอบถาม ไม่ใช่การวินิจฉัยทางการแพทย์หรือการระบุตัวตนที่แท้จริง ไม่มีการจัดเก็บข้อมูลส่วนบุคคลใด ๆ และใช้เพื่อการศึกษาเท่านั้น",
    note: "เครื่องมือนี้ออกแบบมาเพื่อการวิจัยและการศึกษา เพื่อช่วยให้เข้าใจมิติของความหลากหลายทางเพศ",
  },
  en: {
    title: "LGBTQ+ Sexual Fluidity Analysis Tool",
    subtitle: "A research and educational tool to help you understand the dimensions of sexual diversity without collecting personal data. Developed according to research ethics and privacy standards.",
    badge1: "🔒 No Data Collection",
    badge2: "🧠 Statistical",
    badge3: "🎓 Educational",
    badge4: "🌍 SDG 3, 5, 10",
    surveyTitle: "Survey",
    surveyDesc: "Complete the form to analyze trends",
    resultTitle: "Analysis Results",
    resultDesc: "Summary",
    resetBtn: "🔄 Reset",
    submitBtn: "✨ Calculate Results",
    submittingBtn: "⏳ Calculating...",
    errorMsg: "❌ An error occurred during processing. Please try again.",
    successMsg: "✅ Processing successful",
    scoreRange: "Score Range",
    processedAt: "Processed at",
    points: "points",
    noteTitle: "⚠️ Disclaimer",
    refsTitle: "📚 References",
    disclaimer: "These results are statistical trends from survey responses, not a medical diagnosis or identification of true identity. No personal data is collected, and this is for educational purposes only.",
    note: "This tool is designed for research and educational purposes to help understand dimensions of sexual diversity.",
  },
};

// Helper function to translate insights from Thai to English
const translateInsight = (insight: string, language: Language): string => {
  if (language === "th") return insight;
  
  // Translation mappings for common insight patterns
  const translations: Record<string, string> = {
    "🏳️‍🌈 คุณเปิดกว้างและสำรวจความหลากหลายทางเพศในระดับสูง": "🏳️‍🌈 You are open and explore sexual diversity at a high level",
    "🦋 คุณกำลังอยู่ในช่วงสำรวจและเรียนรู้เกี่ยวกับตัวเอง ซึ่งเป็นเรื่องปกติและงดงาม": "🦋 You are in the exploration and learning phase about yourself, which is normal and beautiful",
    "🌱 คุณเริ่มต้นเปิดรับในบางด้าน การค้นหาตัวเองต้องใช้เวลา": "🌱 You are starting to be open in some areas. Self-discovery takes time",
    "🌙 คุณอาจยังไม่สนใจประเด็นนี้ในตอนนี้ และนั่นก็เป็นเรื่องที่ยอมรับได้": "🌙 You may not be interested in this topic right now, and that's acceptable"
  };
  
  // Check for exact match first
  if (translations[insight]) {
    return translations[insight];
  }
  
  // Handle dynamic insights with section names
  const sectionNameMap: Record<string, string> = {
    "การเปิดรับสื่อ": "media exposure",
    "การสนับสนุนจากครอบครัวและเพื่อน": "family and peer support",
    "การมีส่วนร่วมในชุมชนออนไลน์": "online community participation",
    "ปัจจัยด้านวัฒนธรรมและภาษา": "cultural and linguistic factors",
    "การสำรวจตัวตน": "self-exploration",
    "สภาพแวดล้อมทางการศึกษา": "educational environment"
  };
  
  let translated = insight;
  
  // Replace section names
  Object.entries(sectionNameMap).forEach(([thai, english]) => {
    translated = translated.replace(thai, english);
  });
  
  // Replace common phrases
  translated = translated
    .replace(/💡 ปัจจัยที่ควรให้ความสำคัญเพิ่มเติมคือ/g, "💡 Additional factors to consider:")
    .replace(/ด้วยคะแนน/g, "with a score of")
    .replace(/คะแนน/g, "score");
  
  return translated;
};

// Helper function to translate interpretation description
const translateInterpretation = (description: string, language: Language): string => {
  if (language === "th") return description;
  
  const interpretationMap: Record<string, string> = {
    // With "ในระดับ" variations
    "มีการเปิดรับและสำรวจในระดับสูงมาก": "Very high level of openness and exploration",
    "มีการเปิดรับและสำรวจในระดับสูง": "High level of openness and exploration",
    "มีการเปิดรับและสำรวจในระดับปานกลาง": "Moderate level of openness and exploration",
    "มีการเปิดรับและสำรวจในระดับต่ำ": "Low level of openness and exploration",
    "มีการเปิดรับและสำรวจในระดับน้อยมาก": "Minimal level of openness and exploration",
    // Without "ในระดับ" variations (shorter form)
    "มีการเปิดรับและสำรวจสูงมาก": "Very high level of openness and exploration",
    "มีการเปิดรับและสำรวจสูง": "High level of openness and exploration",
    "มีการเปิดรับและสำรวจปานกลาง": "Moderate level of openness and exploration",
    "มีการเปิดรับและสำรวจต่ำ": "Low level of openness and exploration",
    "มีการเปิดรับและสำรวจน้อยมาก": "Minimal level of openness and exploration"
  };
  
  return interpretationMap[description] || description;
};

const questionGroupsData: Record<Language, Array<{
  title: string;
  description: string;
  fields: Array<{
    key: keyof SurveyAnswers;
    label: string;
    options: Array<{ value: number; label: string }>;
  }>;
}>> = {
  th: [
  {
    title: "การเปิดรับสื่อ",
    description: "Media Exposure",
    fields: [
      {
        key: "media1",
        label: "คุณดูซีรีส์วาย (BL) หรือ Yuri (GL) บ่อยแค่ไหน?",
        options: [
          { value: 0, label: "ไม่เคยเลย" },
          { value: 1, label: "เดือนละครั้ง" },
          { value: 2, label: "สัปดาห์ละครั้ง" },
          { value: 3, label: "หลายครั้งต่อสัปดาห์" },
          { value: 4, label: "แทบทุกวัน" },
        ],
      },
      {
        key: "media2",
        label: "คุณติดตามอินฟลูเอนเซอร์ LGBTQ+ หรือไม่?",
        options: [
          { value: 0, label: "ไม่เคย" },
          { value: 1, label: "บางครั้ง" },
          { value: 2, label: "เป็นประจำ" },
          { value: 3, label: "หลายบัญชี" },
          { value: 4, label: "เป็นส่วนหนึ่งของชีวิตประจำวัน" },
        ],
      },
    ],
  },
  {
    title: "ครอบครัวและเพื่อน",
    description: "Family & Peer Support",
    fields: [
      {
        key: "family1",
        label: "ที่บ้านมีสมาชิกที่เป็น LGBTQ+ หรือไม่?",
        options: [
          { value: 0, label: "ไม่มี" },
          { value: 2, label: "มี" },
          { value: 4, label: "มากกว่าหนึ่งคน" },
        ],
      },
      {
        key: "family2",
        label: "ครอบครัวมีทัศนคติต่อ LGBTQ+ อย่างไร?",
        options: [
          { value: 0, label: "ไม่ยอมรับ" },
          { value: 1, label: "คัดค้าน" },
          { value: 2, label: "เฉยๆ" },
          { value: 3, label: "สนับสนุน" },
          { value: 4, label: "สนับสนุนอย่างแข็งขัน" },
        ],
      },
      {
        key: "family3",
        label: "เพื่อนสนิทของคุณมีคนที่เป็น LGBTQ+ หรือไม่?",
        options: [
          { value: 0, label: "ไม่มีเลย" },
          { value: 1, label: "มีอยู่บ้าง" },
          { value: 2, label: "มีหลายคน" },
          { value: 3, label: "ครึ่งหนึ่ง" },
          { value: 4, label: "ส่วนใหญ่" },
        ],
      },
    ],
  },
  {
    title: "ชุมชนออนไลน์",
    description: "Online Community",
    fields: [
      {
        key: "community1",
        label: "คุณเข้าร่วมชุมชนออนไลน์ LGBTQ+ หรือไม่?",
        options: [
          { value: 0, label: "ไม่เคย" },
          { value: 1, label: "เป็นสมาชิกเฉยๆ" },
          { value: 2, label: "เข้าร่วมกิจกรรมบ่อย" },
          { value: 3, label: "เป็นแอดมิน/เจ้าของกลุ่ม" },
          { value: 4, label: "สร้างชุมชนเอง" },
        ],
      },
      {
        key: "community2",
        label: "คุณแชร์เนื้อหา LGBTQ+ ทางโซเชียลบ่อยเพียงใด?",
        options: [
          { value: 0, label: "ไม่เคย" },
          { value: 1, label: "นานๆ ครั้ง" },
          { value: 2, label: "เดือนละครั้ง" },
          { value: 3, label: "สัปดาห์ละครั้ง" },
          { value: 4, label: "หลายครั้งต่อสัปดาห์" },
        ],
      },
    ],
  },
  {
    title: "วัฒนธรรมและภาษา",
    description: "Cultural & Linguistic",
    fields: [
      {
        key: "culture1",
        label: "คุณเข้าใจศัพท์เฉพาะหรือภาษาลูมากน้อยเพียงใด?",
        options: [
          { value: 0, label: "ไม่เข้าใจเลย" },
          { value: 1, label: "พอเข้าใจ" },
          { value: 2, label: "เข้าใจและใช้งานได้" },
          { value: 3, label: "สื่อสารคล่องแคล่ว" },
          { value: 4, label: "ช่วยสอนคนอื่นได้" },
        ],
      },
      {
        key: "culture2",
        label: "คุณสบายใจในการสนทนาเรื่อง LGBTQ+ หรือไม่?",
        options: [
          { value: 0, label: "ไม่สบายใจ" },
          { value: 1, label: "เลี่ยงพูดถึง" },
          { value: 2, label: "พูดได้เมื่อจำเป็น" },
          { value: 3, label: "พูดได้อย่างผ่อนคลาย" },
          { value: 4, label: "พูดได้อย่างมั่นใจ" },
        ],
      },
    ],
  },
  {
    title: "การสำรวจตัวตน",
    description: "Self Exploration",
    fields: [
      {
        key: "exploration1",
        label: "คุณตั้งคำถามเกี่ยวกับรสนิยมทางเพศของตนเองบ่อยเพียงใด?",
        options: [
          { value: 0, label: "ไม่เคย" },
          { value: 1, label: "นานๆ ครั้ง" },
          { value: 2, label: "เป็นครั้งคราว" },
          { value: 3, label: "บ่อย" },
          { value: 4, label: "อยู่ในขั้นสำรวจอย่างจริงจัง" },
        ],
      },
      {
        key: "exploration2",
        label: "คุณรู้สึกดึงดูดกับหลากหลายเพศได้หรือไม่?",
        options: [
          { value: 0, label: "ไม่เลย" },
          { value: 1, label: "บางครั้ง" },
          { value: 2, label: "ขึ้นอยู่กับสถานการณ์" },
          { value: 3, label: "ค่อนข้างใช่" },
          { value: 4, label: "ใช่ชัดเจน" },
        ],
      },
    ],
  },
  {
    title: "สภาพแวดล้อมทางการศึกษา",
    description: "School Environment",
    fields: [
      {
        key: "school1",
        label: "สถานศึกษา/ที่ทำงานของคุณสนับสนุน LGBTQ+ หรือไม่?",
        options: [
          { value: 0, label: "ไม่สนับสนุน" },
          { value: 1, label: "มีแนวทางแต่ไม่จริงจัง" },
          { value: 2, label: "มีนโยบายและกิจกรรมต่อเนื่อง" },
          { value: 3, label: "เป็นผู้นำด้านความหลากหลาย" },
          { value: 4, label: "ได้รับรางวัล/การยอมรับ" },
        ],
      },
    ],
  },
],
en: [
  {
    title: "Media Exposure",
    description: "Exposure to LGBTQ+ content",
    fields: [
      {
        key: "media1",
        label: "How often do you watch BL/GL series?",
        options: [
          { value: 0, label: "Never" },
          { value: 1, label: "Once a month" },
          { value: 2, label: "Once a week" },
          { value: 3, label: "Several times a week" },
          { value: 4, label: "Almost daily" },
        ],
      },
      {
        key: "media2",
        label: "Do you follow LGBTQ+ influencers?",
        options: [
          { value: 0, label: "Never" },
          { value: 1, label: "Sometimes" },
          { value: 2, label: "Regularly" },
          { value: 3, label: "Multiple accounts" },
          { value: 4, label: "Part of daily routine" },
        ],
      },
    ],
  },
  {
    title: "Family & Peer Support",
    description: "Support from family and friends",
    fields: [
      {
        key: "family1",
        label: "Do you have LGBTQ+ family members?",
        options: [
          { value: 0, label: "None" },
          { value: 2, label: "Yes" },
          { value: 4, label: "More than one" },
        ],
      },
      {
        key: "family2",
        label: "How does your family view LGBTQ+ issues?",
        options: [
          { value: 0, label: "Not accepting" },
          { value: 1, label: "Oppose" },
          { value: 2, label: "Neutral" },
          { value: 3, label: "Supportive" },
          { value: 4, label: "Strongly supportive" },
        ],
      },
      {
        key: "family3",
        label: "Do you have LGBTQ+ close friends?",
        options: [
          { value: 0, label: "None" },
          { value: 1, label: "A few" },
          { value: 2, label: "Several" },
          { value: 3, label: "About half" },
          { value: 4, label: "Most" },
        ],
      },
    ],
  },
  {
    title: "Online Community",
    description: "Participation in online spaces",
    fields: [
      {
        key: "community1",
        label: "Do you participate in online LGBTQ+ communities?",
        options: [
          { value: 0, label: "Never" },
          { value: 1, label: "Just a member" },
          { value: 2, label: "Active participant" },
          { value: 3, label: "Admin/moderator" },
          { value: 4, label: "Community creator" },
        ],
      },
      {
        key: "community2",
        label: "How often do you share LGBTQ+ content on social media?",
        options: [
          { value: 0, label: "Never" },
          { value: 1, label: "Rarely" },
          { value: 2, label: "Once a month" },
          { value: 3, label: "Once a week" },
          { value: 4, label: "Several times a week" },
        ],
      },
    ],
  },
  {
    title: "Cultural & Linguistic",
    description: "Understanding of LGBTQ+ culture",
    fields: [
      {
        key: "culture1",
        label: "How well do you understand LGBTQ+ terminology and slang?",
        options: [
          { value: 0, label: "Don't understand" },
          { value: 1, label: "Basic understanding" },
          { value: 2, label: "Understand and use" },
          { value: 3, label: "Fluent" },
          { value: 4, label: "Can teach others" },
        ],
      },
      {
        key: "culture2",
        label: "How comfortable are you discussing LGBTQ+ topics?",
        options: [
          { value: 0, label: "Uncomfortable" },
          { value: 1, label: "Avoid discussing" },
          { value: 2, label: "Can discuss when necessary" },
          { value: 3, label: "Comfortable" },
          { value: 4, label: "Very confident" },
        ],
      },
    ],
  },
  {
    title: "Self Exploration",
    description: "Personal identity exploration",
    fields: [
      {
        key: "exploration1",
        label: "How often do you question your own sexual orientation?",
        options: [
          { value: 0, label: "Never" },
          { value: 1, label: "Rarely" },
          { value: 2, label: "Occasionally" },
          { value: 3, label: "Frequently" },
          { value: 4, label: "Actively exploring" },
        ],
      },
      {
        key: "exploration2",
        label: "Do you feel attracted to multiple genders?",
        options: [
          { value: 0, label: "Not at all" },
          { value: 1, label: "Sometimes" },
          { value: 2, label: "Depends on situation" },
          { value: 3, label: "Somewhat" },
          { value: 4, label: "Yes, clearly" },
        ],
      },
    ],
  },
  {
    title: "School Environment",
    description: "Educational/workplace support",
    fields: [
      {
        key: "school1",
        label: "Does your school/workplace support LGBTQ+ individuals?",
        options: [
          { value: 0, label: "Not supportive" },
          { value: 1, label: "Has policy but not serious" },
          { value: 2, label: "Has ongoing policies and activities" },
          { value: 3, label: "Leader in diversity" },
          { value: 4, label: "Award-winning/recognized" },
        ],
      },
    ],
  },
],
};

const formatTimestamp = (value: string) => new Date(value).toLocaleString();

const sectionLabels: Record<string, { thai: string; en: string; emoji: string }> = {
  media_exposure: { thai: "การเปิดรับสื่อ", en: "Media Exposure", emoji: "📺" },
  family_peer_support: { thai: "ครอบครัวและเพื่อน", en: "Family & Friends", emoji: "👨‍👩‍👧‍👦" },
  online_community: { thai: "ชุมชนออนไลน์", en: "Online Community", emoji: "🌐" },
  cultural_linguistic: { thai: "วัฒนธรรมและภาษา", en: "Culture & Language", emoji: "💬" },
  self_exploration: { thai: "การสำรวจตัวตน", en: "Self Exploration", emoji: "🔍" },
  school_environment: { thai: "สภาพแวดล้อมการศึกษา", en: "Educational Environment", emoji: "🏫" },
};

const SectionCard = ({
  title,
  description,
  children,
}: {
  title: string;
  description: string;
  children: React.ReactNode;
}) => (
  <section className="rounded-3xl border border-pride-200 bg-white/75 p-6 shadow-lg backdrop-blur">
    <header className="mb-4">
      <h2 className="text-xl font-semibold text-pride-800">{title}</h2>
      <p className="text-sm text-pride-600">{description}</p>
    </header>
    {children}
  </section>
);

const ResultCard = ({ result, language }: { result: AnalysisResponse; language: Language }) => {
  const t = translations[language];
  return (
    <SectionCard title={t.resultTitle} description={t.resultDesc}>
    <div className="flex flex-col gap-6">
      <div className="flex flex-col items-center gap-2 rounded-3xl bg-gradient-to-br from-purple-100 via-pink-100 to-rose-100 p-6 shadow-lg">
        <span className="text-6xl font-extrabold bg-gradient-to-r from-purple-600 via-pink-600 to-rose-600 bg-clip-text text-transparent">
          {result.overall_score}%
        </span>
        <p className="text-xl font-bold text-gray-800">
          {result.interpretation.emoji} {translateInterpretation(result.interpretation.description, language)}
        </p>
        <p className="text-xs font-semibold uppercase tracking-wide text-purple-600">
          {t.scoreRange}: {result.interpretation.range}
        </p>
        <p className="text-xs text-gray-500">
          {t.processedAt}: {formatTimestamp(result.timestamp)}
        </p>
      </div>
      <div className="grid gap-3">
        {Object.entries(result.section_scores).map(([key, score]) => {
          const displayPercentage = Math.min(score.percentage, 100);
          const label = sectionLabels[key] || { thai: key, en: key, emoji: "📊" };
          
          // Colorful gradient for each section
          const gradients = [
            "from-purple-400 to-purple-600",
            "from-pink-400 to-pink-600",
            "from-rose-400 to-rose-600",
            "from-orange-400 to-orange-600",
            "from-amber-400 to-amber-600",
            "from-cyan-400 to-cyan-600"
          ];
          const gradientClass = gradients[Object.keys(result.section_scores).indexOf(key) % gradients.length];
          
          return (
            <div key={key} className="rounded-2xl bg-gradient-to-br from-white to-gray-50 p-4 shadow-md transition-all hover:shadow-xl hover:scale-[1.02]">
              <div className="flex items-center justify-between">
                <h3 className="flex items-center gap-2 text-sm font-bold text-gray-800">
                  <span className="text-2xl">{label.emoji}</span>
                  <span>{language === "th" ? label.thai : label.en}</span>
                </h3>
                <span className="text-sm font-bold text-purple-700">
                  {displayPercentage.toFixed(1)}%
                </span>
              </div>
              <div className="mt-3 h-3 rounded-full bg-gray-200 shadow-inner">
                <div
                  className={`h-3 rounded-full bg-gradient-to-r ${gradientClass} shadow-md transition-all duration-700`}
                  style={{ width: `${displayPercentage}%` }}
                />
              </div>
              <p className="mt-2 text-xs font-semibold text-gray-600">
                {score.raw_score} / {score.max_score} {t.points}
              </p>
            </div>
          );
        })}
      </div>
      <div className="grid gap-2">
        {result.insights.map((insight, idx) => (
          <p key={`${insight}-${idx}`} className="rounded-2xl bg-gradient-to-r from-blue-50 to-cyan-50 border border-blue-200 p-4 text-sm font-medium leading-relaxed text-gray-700 shadow-sm">
            {translateInsight(insight, language)}
          </p>
        ))}
      </div>
      <div className="rounded-2xl border-2 border-amber-300 bg-gradient-to-br from-amber-50 to-yellow-50 p-5 shadow-lg">
        <strong className="mb-2 block text-base font-bold text-amber-900">{t.noteTitle}</strong>
        <span className="leading-relaxed text-sm text-amber-800">{t.disclaimer}</span>
      </div>
      <div className="rounded-2xl border-2 border-blue-300 bg-gradient-to-br from-blue-50 to-indigo-50 p-5 shadow-lg">
        <strong className="mb-3 block text-base font-bold text-blue-900">{t.refsTitle}</strong>
        <ul className="list-disc space-y-2 pl-5 leading-relaxed text-sm text-blue-800">
          {result.references.map((ref, idx) => (
            <li key={`${ref}-${idx}`} className="marker:text-blue-500">{ref}</li>
          ))}
        </ul>
      </div>
    </div>
  </SectionCard>
);
};

function App() {
  const [answers, setAnswers] = useState<SurveyAnswers>(initialAnswers);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [language, setLanguage] = useState<Language>("th");

  const t = translations[language];
  const questionGroups = questionGroupsData[language];

  const mutation = useMutation({
    mutationFn: analyzeSurvey,
    onSuccess: (data) => setResult(data),
  });

  const handleChange = (key: keyof SurveyAnswers, value: string) => {
    setAnswers((prev) => ({ ...prev, [key]: Number(value) }));
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    mutation.mutate(answers);
  };

  const handleReset = () => {
    setAnswers(initialAnswers);
    setResult(null);
    mutation.reset();
  };

  return (
    <div className="mx-auto flex min-h-screen max-w-5xl flex-col gap-6 p-6">
      <header className="rounded-3xl bg-gradient-to-br from-purple-500 via-pink-500 to-rose-500 p-10 text-white shadow-2xl">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-5xl animate-pulse">🏳️‍🌈</span>
            <h1 className="text-3xl font-black tracking-tight drop-shadow-lg">{t.title}</h1>
          </div>
          <button
            onClick={() => setLanguage(language === "th" ? "en" : "th")}
            className="rounded-full bg-white px-5 py-2.5 text-sm font-bold text-purple-600 shadow-lg transition-all hover:scale-110 hover:shadow-xl active:scale-95"
            aria-label="Toggle language"
          >
            {language === "th" ? "🇬🇧 EN" : "🇹🇭 TH"}
          </button>
        </div>
        <p className="mt-4 max-w-2xl text-sm leading-relaxed opacity-90">
          {t.subtitle}
        </p>
        <div className="mt-3 flex flex-wrap gap-2 text-xs">
          <span className="rounded-full bg-white px-3 py-1 font-semibold text-purple-600 shadow-md">{t.badge1}</span>
          <span className="rounded-full bg-white px-3 py-1 font-semibold text-pink-600 shadow-md">{t.badge2}</span>
          <span className="rounded-full bg-white px-3 py-1 font-semibold text-rose-600 shadow-md">{t.badge3}</span>
          <span className="rounded-full bg-gradient-to-r from-emerald-400 to-cyan-400 px-3 py-1 font-semibold text-white shadow-md">{t.badge4}</span>
        </div>
      </header>

      <main className="grid gap-6 lg:grid-cols-[2fr,1fr] lg:items-start">
        <SectionCard title={t.surveyTitle} description={t.surveyDesc}>
          <form className="flex flex-col gap-6" onSubmit={handleSubmit}>
            {questionGroups.map((group) => (
              <div key={group.title} className="space-y-4 rounded-2xl bg-gradient-to-br from-pride-50/50 to-white p-5">
                <div>
                  <h3 className="text-lg font-semibold text-pride-700">{group.title}</h3>
                  <p className="text-xs uppercase tracking-wide text-pride-500">{group.description}</p>
                </div>
                <div className="grid gap-4">
                  {group.fields.map((field) => (
                    <label key={field.key} className="grid gap-2">
                      <span className="text-sm font-medium text-pride-800">{field.label}</span>
                      <select
                        value={answers[field.key]}
                        onChange={(event) => handleChange(field.key, event.target.value)}
                        className="rounded-2xl border-2 border-pride-200 bg-white/90 p-3 text-sm shadow-sm transition focus:border-pride-400 focus:outline-none focus:ring-2 focus:ring-pride-200"
                      >
                        {field.options.map((option) => (
                          <Option key={`${field.key}-${option.value}`} value={option.value} label={option.label} />
                        ))}
                      </select>
                    </label>
                  ))}
                </div>
              </div>
            ))}
            <div className="flex flex-col gap-3 md:flex-row md:justify-end">
              <button
                type="button"
                onClick={handleReset}
                className="rounded-full border-2 border-rose-400 bg-white px-6 py-3 text-sm font-bold text-rose-600 shadow-md transition-all hover:bg-rose-50 hover:border-rose-500 hover:shadow-lg hover:scale-105 active:scale-95"
              >
                {t.resetBtn}
              </button>
              <button
                type="submit"
                disabled={mutation.isPending}
                className="rounded-full bg-gradient-to-r from-emerald-500 via-teal-500 to-cyan-500 px-8 py-3 text-sm font-bold text-white shadow-xl transition-all hover:shadow-2xl hover:scale-105 active:scale-95 disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:scale-100"
              >
                {mutation.isPending ? t.submittingBtn : t.submitBtn}
              </button>
            </div>
            {mutation.isError && (
              <p className="rounded-2xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
                {t.errorMsg}
              </p>
            )}
            {mutation.isSuccess && (
              <p className="rounded-2xl border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">
                {t.successMsg}
              </p>
            )}
          </form>
        </SectionCard>

        {result && (
          <div className="space-y-6 lg:sticky lg:top-6 lg:max-h-[calc(100vh-8rem)] lg:overflow-y-auto">
            <ResultCard result={result} language={language} />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
