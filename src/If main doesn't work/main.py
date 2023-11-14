import io
import sys
import time
import random
import sqlite3
import word_level_list  # Файс со словами/цитатими/уровнями

from PyQt5.QtWidgets import QApplication, QMainWindow 
from PyQt5 import QtCore, QtWidgets, uic

# Знаю, что можно было сделать умнее и чище(Полиморфизм?!), но теперь я понимаю, что нужно продумывать структуру заранее и писать не за 4 дня перед дедлайном :) 
template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>1200</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>FastTyping</string>
  </property>
  <property name="windowIcon">
   <iconset>
    <normaloff>images/keybord.png</normaloff>images/keybord.png</iconset>
  </property>
  <property name="windowOpacity">
   <double>1.000000000000000</double>
  </property>
  <property name="styleSheet">
   <string notr="true">background-color: rgb(50,52,55);</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <property name="enabled">
    <bool>true</bool>
   </property>
   <property name="palette">
    <palette>
     <active>
      <colorrole role="Button">
       <brush brushstyle="SolidPattern">
        <color alpha="255">
         <red>50</red>
         <green>52</green>
         <blue>55</blue>
        </color>
       </brush>
      </colorrole>
      <colorrole role="Base">
       <brush brushstyle="SolidPattern">
        <color alpha="255">
         <red>50</red>
         <green>52</green>
         <blue>55</blue>
        </color>
       </brush>
      </colorrole>
      <colorrole role="Window">
       <brush brushstyle="SolidPattern">
        <color alpha="255">
         <red>50</red>
         <green>52</green>
         <blue>55</blue>
        </color>
       </brush>
      </colorrole>
     </active>
     <inactive>
      <colorrole role="Button">
       <brush brushstyle="SolidPattern">
        <color alpha="255">
         <red>50</red>
         <green>52</green>
         <blue>55</blue>
        </color>
       </brush>
      </colorrole>
      <colorrole role="Base">
       <brush brushstyle="SolidPattern">
        <color alpha="255">
         <red>50</red>
         <green>52</green>
         <blue>55</blue>
        </color>
       </brush>
      </colorrole>
      <colorrole role="Window">
       <brush brushstyle="SolidPattern">
        <color alpha="255">
         <red>50</red>
         <green>52</green>
         <blue>55</blue>
        </color>
       </brush>
      </colorrole>
     </inactive>
     <disabled>
      <colorrole role="Button">
       <brush brushstyle="SolidPattern">
        <color alpha="255">
         <red>50</red>
         <green>52</green>
         <blue>55</blue>
        </color>
       </brush>
      </colorrole>
      <colorrole role="Base">
       <brush brushstyle="SolidPattern">
        <color alpha="255">
         <red>50</red>
         <green>52</green>
         <blue>55</blue>
        </color>
       </brush>
      </colorrole>
      <colorrole role="Window">
       <brush brushstyle="SolidPattern">
        <color alpha="255">
         <red>50</red>
         <green>52</green>
         <blue>55</blue>
        </color>
       </brush>
      </colorrole>
     </disabled>
    </palette>
   </property>
   <property name="styleSheet">
    <string notr="true"/>
   </property>
   <widget class="QPushButton" name="Button_Training">
    <property name="geometry">
     <rect>
      <x>450</x>
      <y>20</y>
      <width>300</width>
      <height>90</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <family>Microsoft Sans Serif</family>
      <pointsize>30</pointsize>
      <weight>50</weight>
      <bold>false</bold>
      <stylestrategy>PreferDefault</stylestrategy>
      <kerning>false</kerning>
     </font>
    </property>
    <property name="styleSheet">
     <string notr="true">color: rgb(100, 102, 105);</string>
    </property>
    <property name="text">
     <string>Обучение</string>
    </property>
   </widget>
   <widget class="QPushButton" name="Button_Practice">
    <property name="geometry">
     <rect>
      <x>80</x>
      <y>20</y>
      <width>300</width>
      <height>90</height>
     </rect>
    </property>
    <property name="sizePolicy">
     <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
      <horstretch>0</horstretch>
      <verstretch>0</verstretch>
     </sizepolicy>
    </property>
    <property name="baseSize">
     <size>
      <width>0</width>
      <height>0</height>
     </size>
    </property>
    <property name="font">
     <font>
      <family>Microsoft Sans Serif</family>
      <pointsize>30</pointsize>
     </font>
    </property>
    <property name="styleSheet">
     <string notr="true">color: rgb(100, 102, 105);
</string>
    </property>
    <property name="inputMethodHints">
     <set>Qt::ImhNone</set>
    </property>
    <property name="text">
     <string>Практика</string>
    </property>
    <property name="autoDefault">
     <bool>false</bool>
    </property>
    <property name="default">
     <bool>false</bool>
    </property>
    <property name="flat">
     <bool>false</bool>
    </property>
   </widget>
   <widget class="QPushButton" name="Button_Profile">
    <property name="enabled">
     <bool>true</bool>
    </property>
    <property name="geometry">
     <rect>
      <x>820</x>
      <y>20</y>
      <width>300</width>
      <height>90</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <family>Microsoft Sans Serif</family>
      <pointsize>30</pointsize>
     </font>
    </property>
    <property name="styleSheet">
     <string notr="true">color: rgb(100, 102, 105);</string>
    </property>
    <property name="text">
     <string>Профиль</string>
    </property>
   </widget>
   <widget class="QStackedWidget" name="stackedWidget">
    <property name="geometry">
     <rect>
      <x>50</x>
      <y>190</y>
      <width>1100</width>
      <height>400</height>
     </rect>
    </property>
    <property name="sizePolicy">
     <sizepolicy hsizetype="Preferred" vsizetype="Preferred">
      <horstretch>0</horstretch>
      <verstretch>100</verstretch>
     </sizepolicy>
    </property>
    <property name="currentIndex">
     <number>3</number>
    </property>
    <widget class="QWidget" name="Practice_page">
     <widget class="QLineEdit" name="lineEditPractice">
      <property name="geometry">
       <rect>
        <x>300</x>
        <y>250</y>
        <width>520</width>
        <height>51</height>
       </rect>
      </property>
      <property name="font">
       <font>
        <family>Microsoft Sans Serif</family>
        <pointsize>20</pointsize>
       </font>
      </property>
      <property name="styleSheet">
       <string notr="true">color: rgb(100, 102, 105);</string>
      </property>
     </widget>
     <widget class="QTextBrowser" name="textBrowserPracticeEdit">
      <property name="geometry">
       <rect>
        <x>190</x>
        <y>10</y>
        <width>740</width>
        <height>221</height>
       </rect>
      </property>
      <property name="font">
       <font>
        <family>Microsoft Sans Serif</family>
        <pointsize>20</pointsize>
       </font>
      </property>
      <property name="styleSheet">
       <string notr="true">border: 0;
color: rgb(100, 102, 105);
background: transparent;</string>
      </property>
      <property name="html">
       <string notr="true">&lt;!DOCTYPE HTML PUBLIC &quot;-//W3C//DTD HTML 4.0//EN&quot; &quot;http://www.w3.org/TR/REC-html40/strict.dtd&quot;&gt;
&lt;html&gt;&lt;head&gt;&lt;meta name=&quot;qrichtext&quot; content=&quot;1&quot; /&gt;&lt;style type=&quot;text/css&quot;&gt;
p, li { white-space: pre-wrap; }
&lt;/style&gt;&lt;/head&gt;&lt;body style=&quot; font-family:'Microsoft Sans Serif'; font-size:20pt; font-weight:400; font-style:normal;&quot;&gt;
&lt;p style=&quot;-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2';&quot;&gt;&lt;br /&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
      </property>
      <property name="overwriteMode">
       <bool>true</bool>
      </property>
     </widget>
     <widget class="QTextBrowser" name="textBrowserPracticeSolid">
      <property name="geometry">
       <rect>
        <x>190</x>
        <y>10</y>
        <width>740</width>
        <height>221</height>
       </rect>
      </property>
      <property name="font">
       <font>
        <family>Microsoft Sans Serif</family>
        <pointsize>20</pointsize>
       </font>
      </property>
      <property name="styleSheet">
       <string notr="true">border: 0;
color: rgb(100, 102, 105);
</string>
      </property>
      <property name="verticalScrollBarPolicy">
       <enum>Qt::ScrollBarAlwaysOff</enum>
      </property>
      <property name="horizontalScrollBarPolicy">
       <enum>Qt::ScrollBarAlwaysOff</enum>
      </property>
      <property name="html">
       <string notr="true">&lt;!DOCTYPE HTML PUBLIC &quot;-//W3C//DTD HTML 4.0//EN&quot; &quot;http://www.w3.org/TR/REC-html40/strict.dtd&quot;&gt;
&lt;html&gt;&lt;head&gt;&lt;meta name=&quot;qrichtext&quot; content=&quot;1&quot; /&gt;&lt;style type=&quot;text/css&quot;&gt;
p, li { white-space: pre-wrap; }
&lt;/style&gt;&lt;/head&gt;&lt;body style=&quot; font-family:'Microsoft Sans Serif'; font-size:20pt; font-weight:400; font-style:normal;&quot;&gt;
&lt;p style=&quot;-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2';&quot;&gt;&lt;br /&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
      </property>
      <property name="overwriteMode">
       <bool>true</bool>
      </property>
     </widget>
     <widget class="QWidget" name="">
      <property name="geometry">
       <rect>
        <x>470</x>
        <y>340</y>
        <width>158</width>
        <height>30</height>
       </rect>
      </property>
      <layout class="QHBoxLayout" name="horizontalLayout">
       <item>
        <widget class="QPushButton" name="Button_Quote">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="baseSize">
          <size>
           <width>0</width>
           <height>0</height>
          </size>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>12</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="inputMethodHints">
          <set>Qt::ImhNone</set>
         </property>
         <property name="text">
          <string>Цитаты</string>
         </property>
         <property name="autoDefault">
          <bool>false</bool>
         </property>
         <property name="default">
          <bool>false</bool>
         </property>
         <property name="flat">
          <bool>false</bool>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QPushButton" name="Button_Words">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="baseSize">
          <size>
           <width>0</width>
           <height>0</height>
          </size>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>12</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="inputMethodHints">
          <set>Qt::ImhNone</set>
         </property>
         <property name="text">
          <string>Слова</string>
         </property>
         <property name="autoDefault">
          <bool>false</bool>
         </property>
         <property name="default">
          <bool>false</bool>
         </property>
         <property name="flat">
          <bool>false</bool>
         </property>
        </widget>
       </item>
      </layout>
     </widget>
     <zorder>lineEditPractice</zorder>
     <zorder>textBrowserPracticeSolid</zorder>
     <zorder>textBrowserPracticeEdit</zorder>
     <zorder>Button_Quote</zorder>
     <zorder>Button_Words</zorder>
    </widget>
    <widget class="QWidget" name="TrainingIn_page">
     <widget class="QTextBrowser" name="textBrowserTrainingSolid">
      <property name="geometry">
       <rect>
        <x>260</x>
        <y>40</y>
        <width>740</width>
        <height>221</height>
       </rect>
      </property>
      <property name="font">
       <font>
        <family>Microsoft Sans Serif</family>
        <pointsize>20</pointsize>
       </font>
      </property>
      <property name="styleSheet">
       <string notr="true">border: 0;
color: rgb(100, 102, 105);
</string>
      </property>
      <property name="verticalScrollBarPolicy">
       <enum>Qt::ScrollBarAlwaysOff</enum>
      </property>
      <property name="horizontalScrollBarPolicy">
       <enum>Qt::ScrollBarAlwaysOff</enum>
      </property>
      <property name="html">
       <string notr="true">&lt;!DOCTYPE HTML PUBLIC &quot;-//W3C//DTD HTML 4.0//EN&quot; &quot;http://www.w3.org/TR/REC-html40/strict.dtd&quot;&gt;
&lt;html&gt;&lt;head&gt;&lt;meta name=&quot;qrichtext&quot; content=&quot;1&quot; /&gt;&lt;style type=&quot;text/css&quot;&gt;
p, li { white-space: pre-wrap; }
&lt;/style&gt;&lt;/head&gt;&lt;body style=&quot; font-family:'Microsoft Sans Serif'; font-size:20pt; font-weight:400; font-style:normal;&quot;&gt;
&lt;p style=&quot;-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2';&quot;&gt;&lt;br /&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
      </property>
      <property name="overwriteMode">
       <bool>true</bool>
      </property>
     </widget>
     <widget class="QTextBrowser" name="textBrowserTrainingEdit">
      <property name="geometry">
       <rect>
        <x>260</x>
        <y>40</y>
        <width>740</width>
        <height>221</height>
       </rect>
      </property>
      <property name="font">
       <font>
        <family>Microsoft Sans Serif</family>
        <pointsize>20</pointsize>
       </font>
      </property>
      <property name="styleSheet">
       <string notr="true">border: 0;
color: rgb(100, 102, 105);
background: transparent;</string>
      </property>
      <property name="html">
       <string notr="true">&lt;!DOCTYPE HTML PUBLIC &quot;-//W3C//DTD HTML 4.0//EN&quot; &quot;http://www.w3.org/TR/REC-html40/strict.dtd&quot;&gt;
&lt;html&gt;&lt;head&gt;&lt;meta name=&quot;qrichtext&quot; content=&quot;1&quot; /&gt;&lt;style type=&quot;text/css&quot;&gt;
p, li { white-space: pre-wrap; }
&lt;/style&gt;&lt;/head&gt;&lt;body style=&quot; font-family:'Microsoft Sans Serif'; font-size:20pt; font-weight:400; font-style:normal;&quot;&gt;
&lt;p style=&quot;-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2';&quot;&gt;&lt;br /&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
      </property>
      <property name="overwriteMode">
       <bool>true</bool>
      </property>
     </widget>
     <widget class="QLineEdit" name="lineEditTraining">
      <property name="geometry">
       <rect>
        <x>230</x>
        <y>110</y>
        <width>651</width>
        <height>51</height>
       </rect>
      </property>
      <property name="font">
       <font>
        <family>Microsoft Sans Serif</family>
        <pointsize>20</pointsize>
       </font>
      </property>
      <property name="styleSheet">
       <string notr="true">color: rgb(100, 102, 105);</string>
      </property>
     </widget>
     <widget class="QGroupBox" name="groupBox">
      <property name="geometry">
       <rect>
        <x>170</x>
        <y>170</y>
        <width>761</width>
        <height>231</height>
       </rect>
      </property>
      <property name="styleSheet">
       <string notr="true">border: none;
</string>
      </property>
      <property name="title">
       <string/>
      </property>
      <widget class="QLabel" name="label_13">
       <property name="geometry">
        <rect>
         <x>110</x>
         <y>100</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">color: rgb(100, 102, 105);
border: 1px solid grey;
background-color: rgb(255, 211, 203);</string>
       </property>
       <property name="text">
        <string>ф</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_26">
       <property name="geometry">
        <rect>
         <x>220</x>
         <y>140</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(196, 255, 133);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>с</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_4">
       <property name="geometry">
        <rect>
         <x>160</x>
         <y>20</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">color: rgb(100, 102, 105);
background-color: rgb(196, 255, 133);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>3</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_16">
       <property name="geometry">
        <rect>
         <x>230</x>
         <y>100</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(88, 191, 255);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>а</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_30">
       <property name="geometry">
        <rect>
         <x>380</x>
         <y>140</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(245, 166, 255);
color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>ь</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_2">
       <property name="geometry">
        <rect>
         <x>80</x>
         <y>20</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 211, 203);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>1</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_22">
       <property name="geometry">
        <rect>
         <x>470</x>
         <y>100</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 211, 203);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>ж</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_29">
       <property name="geometry">
        <rect>
         <x>340</x>
         <y>140</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(245, 166, 255);
color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>т</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_15">
       <property name="geometry">
        <rect>
         <x>190</x>
         <y>100</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(196, 255, 133);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>в</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_9">
       <property name="geometry">
        <rect>
         <x>360</x>
         <y>20</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(196, 255, 133);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>8</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_12">
       <property name="geometry">
        <rect>
         <x>480</x>
         <y>20</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 211, 203);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>-</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_33">
       <property name="geometry">
        <rect>
         <x>500</x>
         <y>140</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 211, 203);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>.,</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_31">
       <property name="geometry">
        <rect>
         <x>420</x>
         <y>140</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(196, 255, 133);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>б</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_27">
       <property name="geometry">
        <rect>
         <x>260</x>
         <y>140</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(88, 191, 255);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>м</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_19">
       <property name="geometry">
        <rect>
         <x>350</x>
         <y>100</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(245, 166, 255);
color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>о</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_18">
       <property name="geometry">
        <rect>
         <x>310</x>
         <y>100</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(245, 166, 255);
color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>р</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_25">
       <property name="geometry">
        <rect>
         <x>180</x>
         <y>140</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 233, 176);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>ч</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_10">
       <property name="geometry">
        <rect>
         <x>400</x>
         <y>20</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 233, 176);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>9</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_7">
       <property name="geometry">
        <rect>
         <x>280</x>
         <y>20</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(245, 166, 255);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>6</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_23">
       <property name="geometry">
        <rect>
         <x>510</x>
         <y>100</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 211, 203);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>э</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label">
       <property name="geometry">
        <rect>
         <x>40</x>
         <y>20</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 211, 203);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>Ё</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_17">
       <property name="geometry">
        <rect>
         <x>270</x>
         <y>100</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(88, 191, 255);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>п</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_11">
       <property name="geometry">
        <rect>
         <x>440</x>
         <y>20</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 211, 203);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>0</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_21">
       <property name="geometry">
        <rect>
         <x>430</x>
         <y>100</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 233, 176);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>д</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_5">
       <property name="geometry">
        <rect>
         <x>200</x>
         <y>20</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(88, 191, 255);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>4</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_3">
       <property name="geometry">
        <rect>
         <x>120</x>
         <y>20</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">color: rgb(100, 102, 105);
background-color: rgb(255, 233, 176);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>2</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_14">
       <property name="geometry">
        <rect>
         <x>150</x>
         <y>100</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 233, 176);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>ы</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_20">
       <property name="geometry">
        <rect>
         <x>390</x>
         <y>100</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(196, 255, 133);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>л</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_32">
       <property name="geometry">
        <rect>
         <x>460</x>
         <y>140</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 233, 176);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>ю</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_24">
       <property name="geometry">
        <rect>
         <x>140</x>
         <y>140</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">color: rgb(100, 102, 105);
border: 1px solid grey;
background-color: rgb(255, 211, 203);</string>
       </property>
       <property name="text">
        <string>я</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_8">
       <property name="geometry">
        <rect>
         <x>320</x>
         <y>20</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(245, 166, 255);
color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>7</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_28">
       <property name="geometry">
        <rect>
         <x>300</x>
         <y>140</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(88, 191, 255);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>и</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_6">
       <property name="geometry">
        <rect>
         <x>240</x>
         <y>20</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(88, 191, 255);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>5</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_34">
       <property name="geometry">
        <rect>
         <x>540</x>
         <y>60</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 211, 203);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>ъ</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_35">
       <property name="geometry">
        <rect>
         <x>180</x>
         <y>60</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(196, 255, 133);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>у</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_36">
       <property name="geometry">
        <rect>
         <x>460</x>
         <y>60</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 211, 203);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>з</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_37">
       <property name="geometry">
        <rect>
         <x>380</x>
         <y>60</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(196, 255, 133);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>ш</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_38">
       <property name="geometry">
        <rect>
         <x>100</x>
         <y>60</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 211, 203);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>й</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_39">
       <property name="geometry">
        <rect>
         <x>500</x>
         <y>60</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 211, 203);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>х</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_40">
       <property name="geometry">
        <rect>
         <x>220</x>
         <y>60</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">color: rgb(100, 102, 105);
background-color: rgb(88, 191, 255);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>к</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_41">
       <property name="geometry">
        <rect>
         <x>300</x>
         <y>60</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">color: rgb(100, 102, 105);
background-color: rgb(245, 166, 255);

border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>н</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_42">
       <property name="geometry">
        <rect>
         <x>260</x>
         <y>60</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(88, 191, 255);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>е</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_43">
       <property name="geometry">
        <rect>
         <x>340</x>
         <y>60</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(245, 166, 255);
color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>г</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_44">
       <property name="geometry">
        <rect>
         <x>140</x>
         <y>60</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 233, 176);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>ц</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_45">
       <property name="geometry">
        <rect>
         <x>420</x>
         <y>60</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 233, 176);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>щ</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_46">
       <property name="geometry">
        <rect>
         <x>520</x>
         <y>20</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 211, 203);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>+</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_47">
       <property name="geometry">
        <rect>
         <x>40</x>
         <y>60</y>
         <width>51</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 211, 203);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>Tab</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_48">
       <property name="geometry">
        <rect>
         <x>40</x>
         <y>100</y>
         <width>61</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">color: rgb(100, 102, 105);
background-color: rgb(255, 211, 203);border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>Caps</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_49">
       <property name="geometry">
        <rect>
         <x>40</x>
         <y>140</y>
         <width>91</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">color: rgb(100, 102, 105);
border: 1px solid grey;
background-color: rgb(255, 211, 203);</string>
       </property>
       <property name="text">
        <string>Shift</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_50">
       <property name="geometry">
        <rect>
         <x>200</x>
         <y>180</y>
         <width>211</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">color: rgb(100, 102, 105);
background-color: rgb(255, 64, 64);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>Space</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_52">
       <property name="geometry">
        <rect>
         <x>150</x>
         <y>180</y>
         <width>41</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>Alt</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_53">
       <property name="geometry">
        <rect>
         <x>90</x>
         <y>180</y>
         <width>51</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>Win</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_54">
       <property name="geometry">
        <rect>
         <x>40</x>
         <y>180</y>
         <width>41</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>Ctrl</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_55">
       <property name="geometry">
        <rect>
         <x>420</x>
         <y>180</y>
         <width>41</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>Alt</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_56">
       <property name="geometry">
        <rect>
         <x>470</x>
         <y>180</y>
         <width>41</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>Win</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_57">
       <property name="geometry">
        <rect>
         <x>520</x>
         <y>180</y>
         <width>41</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>Fn</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_58">
       <property name="geometry">
        <rect>
         <x>570</x>
         <y>180</y>
         <width>41</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>Ctlr</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_59">
       <property name="geometry">
        <rect>
         <x>540</x>
         <y>140</y>
         <width>71</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 211, 203);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>Shift</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_60">
       <property name="geometry">
        <rect>
         <x>550</x>
         <y>100</y>
         <width>61</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 211, 203);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>Enter</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_61">
       <property name="geometry">
        <rect>
         <x>580</x>
         <y>60</y>
         <width>31</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 211, 203);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>\</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_62">
       <property name="geometry">
        <rect>
         <x>560</x>
         <y>20</y>
         <width>51</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>14</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 211, 203);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>Back</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_51">
       <property name="geometry">
        <rect>
         <x>630</x>
         <y>20</y>
         <width>121</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>12</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 211, 203);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>Мизинец</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_63">
       <property name="geometry">
        <rect>
         <x>630</x>
         <y>60</y>
         <width>121</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>10</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(255, 233, 176);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>Безымянный</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_64">
       <property name="geometry">
        <rect>
         <x>630</x>
         <y>100</y>
         <width>121</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>10</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(196, 255, 133);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>Средний</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_65">
       <property name="geometry">
        <rect>
         <x>630</x>
         <y>140</y>
         <width>121</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>8</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(245, 166, 255);
color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>Указательный правый</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
      <widget class="QLabel" name="label_66">
       <property name="geometry">
        <rect>
         <x>630</x>
         <y>180</y>
         <width>121</width>
         <height>31</height>
        </rect>
       </property>
       <property name="font">
        <font>
         <family>Microsoft Sans Serif</family>
         <pointsize>8</pointsize>
        </font>
       </property>
       <property name="styleSheet">
        <string notr="true">background-color: rgb(88, 191, 255);color: rgb(100, 102, 105);
border: 1px solid grey;
</string>
       </property>
       <property name="text">
        <string>Указательный левый</string>
       </property>
       <property name="alignment">
        <set>Qt::AlignCenter</set>
       </property>
      </widget>
     </widget>
    </widget>
    <widget class="QWidget" name="TrainingOut_page">
     <widget class="QWidget" name="">
      <property name="geometry">
       <rect>
        <x>0</x>
        <y>20</y>
        <width>1101</width>
        <height>351</height>
       </rect>
      </property>
      <layout class="QGridLayout" name="gridLayout">
       <item row="3" column="0">
        <widget class="QPushButton" name="level_11">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="baseSize">
          <size>
           <width>0</width>
           <height>0</height>
          </size>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>30</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="inputMethodHints">
          <set>Qt::ImhNone</set>
         </property>
         <property name="text">
          <string>Урок 11</string>
         </property>
         <property name="autoDefault">
          <bool>false</bool>
         </property>
         <property name="default">
          <bool>false</bool>
         </property>
         <property name="flat">
          <bool>false</bool>
         </property>
        </widget>
       </item>
       <item row="0" column="3">
        <widget class="QPushButton" name="level_4">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="baseSize">
          <size>
           <width>0</width>
           <height>0</height>
          </size>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>30</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="inputMethodHints">
          <set>Qt::ImhNone</set>
         </property>
         <property name="text">
          <string>Урок 4</string>
         </property>
         <property name="autoDefault">
          <bool>false</bool>
         </property>
         <property name="default">
          <bool>false</bool>
         </property>
         <property name="flat">
          <bool>false</bool>
         </property>
        </widget>
       </item>
       <item row="3" column="1">
        <widget class="QPushButton" name="level_12">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="baseSize">
          <size>
           <width>0</width>
           <height>0</height>
          </size>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>30</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="inputMethodHints">
          <set>Qt::ImhNone</set>
         </property>
         <property name="text">
          <string>Урок 12</string>
         </property>
         <property name="autoDefault">
          <bool>false</bool>
         </property>
         <property name="default">
          <bool>false</bool>
         </property>
         <property name="flat">
          <bool>false</bool>
         </property>
        </widget>
       </item>
       <item row="3" column="2">
        <widget class="QPushButton" name="level_13">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="baseSize">
          <size>
           <width>0</width>
           <height>0</height>
          </size>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>30</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="inputMethodHints">
          <set>Qt::ImhNone</set>
         </property>
         <property name="text">
          <string>Урок 13</string>
         </property>
         <property name="autoDefault">
          <bool>false</bool>
         </property>
         <property name="default">
          <bool>false</bool>
         </property>
         <property name="flat">
          <bool>false</bool>
         </property>
        </widget>
       </item>
       <item row="0" column="0">
        <widget class="QPushButton" name="level_1">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="baseSize">
          <size>
           <width>0</width>
           <height>0</height>
          </size>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>30</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="inputMethodHints">
          <set>Qt::ImhNone</set>
         </property>
         <property name="text">
          <string>Урок 1</string>
         </property>
         <property name="autoDefault">
          <bool>false</bool>
         </property>
         <property name="default">
          <bool>false</bool>
         </property>
         <property name="flat">
          <bool>false</bool>
         </property>
        </widget>
       </item>
       <item row="2" column="0">
        <widget class="QPushButton" name="level_6">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="baseSize">
          <size>
           <width>0</width>
           <height>0</height>
          </size>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>30</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="inputMethodHints">
          <set>Qt::ImhNone</set>
         </property>
         <property name="text">
          <string>Урок 6</string>
         </property>
         <property name="autoDefault">
          <bool>false</bool>
         </property>
         <property name="default">
          <bool>false</bool>
         </property>
         <property name="flat">
          <bool>false</bool>
         </property>
        </widget>
       </item>
       <item row="3" column="3">
        <widget class="QPushButton" name="level_14">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="baseSize">
          <size>
           <width>0</width>
           <height>0</height>
          </size>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>30</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="inputMethodHints">
          <set>Qt::ImhNone</set>
         </property>
         <property name="text">
          <string>Урок 14</string>
         </property>
         <property name="autoDefault">
          <bool>false</bool>
         </property>
         <property name="default">
          <bool>false</bool>
         </property>
         <property name="flat">
          <bool>false</bool>
         </property>
        </widget>
       </item>
       <item row="2" column="2">
        <widget class="QPushButton" name="level_8">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="baseSize">
          <size>
           <width>0</width>
           <height>0</height>
          </size>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>30</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="inputMethodHints">
          <set>Qt::ImhNone</set>
         </property>
         <property name="text">
          <string>Урок 8</string>
         </property>
         <property name="autoDefault">
          <bool>false</bool>
         </property>
         <property name="default">
          <bool>false</bool>
         </property>
         <property name="flat">
          <bool>false</bool>
         </property>
        </widget>
       </item>
       <item row="2" column="3">
        <widget class="QPushButton" name="level_9">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="baseSize">
          <size>
           <width>0</width>
           <height>0</height>
          </size>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>30</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="inputMethodHints">
          <set>Qt::ImhNone</set>
         </property>
         <property name="text">
          <string>Урок 9</string>
         </property>
         <property name="autoDefault">
          <bool>false</bool>
         </property>
         <property name="default">
          <bool>false</bool>
         </property>
         <property name="flat">
          <bool>false</bool>
         </property>
        </widget>
       </item>
       <item row="0" column="1">
        <widget class="QPushButton" name="level_2">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="baseSize">
          <size>
           <width>0</width>
           <height>0</height>
          </size>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>30</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="inputMethodHints">
          <set>Qt::ImhNone</set>
         </property>
         <property name="text">
          <string>Урок 2</string>
         </property>
         <property name="autoDefault">
          <bool>false</bool>
         </property>
         <property name="default">
          <bool>false</bool>
         </property>
         <property name="flat">
          <bool>false</bool>
         </property>
        </widget>
       </item>
       <item row="2" column="4">
        <widget class="QPushButton" name="level_10">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="baseSize">
          <size>
           <width>0</width>
           <height>0</height>
          </size>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>30</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="inputMethodHints">
          <set>Qt::ImhNone</set>
         </property>
         <property name="text">
          <string>Урок 10</string>
         </property>
         <property name="autoDefault">
          <bool>false</bool>
         </property>
         <property name="default">
          <bool>false</bool>
         </property>
         <property name="flat">
          <bool>false</bool>
         </property>
        </widget>
       </item>
       <item row="2" column="1">
        <widget class="QPushButton" name="level_7">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="baseSize">
          <size>
           <width>0</width>
           <height>0</height>
          </size>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>30</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="inputMethodHints">
          <set>Qt::ImhNone</set>
         </property>
         <property name="text">
          <string>Урок 7</string>
         </property>
         <property name="autoDefault">
          <bool>false</bool>
         </property>
         <property name="default">
          <bool>false</bool>
         </property>
         <property name="flat">
          <bool>false</bool>
         </property>
        </widget>
       </item>
       <item row="3" column="4">
        <widget class="QPushButton" name="level_15">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="baseSize">
          <size>
           <width>0</width>
           <height>0</height>
          </size>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>30</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="inputMethodHints">
          <set>Qt::ImhNone</set>
         </property>
         <property name="text">
          <string>Урок 15</string>
         </property>
         <property name="autoDefault">
          <bool>false</bool>
         </property>
         <property name="default">
          <bool>false</bool>
         </property>
         <property name="flat">
          <bool>false</bool>
         </property>
        </widget>
       </item>
       <item row="0" column="2">
        <widget class="QPushButton" name="level_3">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="baseSize">
          <size>
           <width>0</width>
           <height>0</height>
          </size>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>30</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="inputMethodHints">
          <set>Qt::ImhNone</set>
         </property>
         <property name="text">
          <string>Урок 3</string>
         </property>
         <property name="autoDefault">
          <bool>false</bool>
         </property>
         <property name="default">
          <bool>false</bool>
         </property>
         <property name="flat">
          <bool>false</bool>
         </property>
        </widget>
       </item>
       <item row="0" column="4">
        <widget class="QPushButton" name="level_5">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="baseSize">
          <size>
           <width>0</width>
           <height>0</height>
          </size>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>30</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="inputMethodHints">
          <set>Qt::ImhNone</set>
         </property>
         <property name="text">
          <string>Урок 5</string>
         </property>
         <property name="autoDefault">
          <bool>false</bool>
         </property>
         <property name="default">
          <bool>false</bool>
         </property>
         <property name="flat">
          <bool>false</bool>
         </property>
        </widget>
       </item>
      </layout>
     </widget>
    </widget>
    <widget class="QWidget" name="Profile_page">
     <widget class="QPushButton" name="Button_ClearInfo">
      <property name="geometry">
       <rect>
        <x>410</x>
        <y>350</y>
        <width>201</width>
        <height>41</height>
       </rect>
      </property>
      <property name="font">
       <font>
        <family>Microsoft Sans Serif</family>
        <pointsize>20</pointsize>
        <weight>50</weight>
        <bold>false</bold>
        <stylestrategy>PreferDefault</stylestrategy>
        <kerning>false</kerning>
       </font>
      </property>
      <property name="styleSheet">
       <string notr="true">color: rgb(100, 102, 105);</string>
      </property>
      <property name="text">
       <string>Очистить</string>
      </property>
     </widget>
     <widget class="QWidget" name="">
      <property name="geometry">
       <rect>
        <x>20</x>
        <y>20</y>
        <width>961</width>
        <height>321</height>
       </rect>
      </property>
      <layout class="QGridLayout" name="gridLayout_2">
       <item row="0" column="1">
        <widget class="QLabel" name="accuracy">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Ignored" vsizetype="Ignored">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>20</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="text">
          <string>TextLabel</string>
         </property>
         <property name="alignment">
          <set>Qt::AlignCenter</set>
         </property>
        </widget>
       </item>
       <item row="1" column="0" colspan="2">
        <widget class="QLabel" name="timeTyping">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Ignored" vsizetype="Ignored">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>20</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="text">
          <string>TextLabel</string>
         </property>
         <property name="alignment">
          <set>Qt::AlignCenter</set>
         </property>
        </widget>
       </item>
       <item row="0" column="0">
        <widget class="QLabel" name="countCompletedTests">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Ignored" vsizetype="Ignored">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>20</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="text">
          <string>TextLabel</string>
         </property>
         <property name="alignment">
          <set>Qt::AlignCenter</set>
         </property>
        </widget>
       </item>
       <item row="2" column="1">
        <widget class="QLabel" name="maxSpeed">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Ignored" vsizetype="Ignored">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>20</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="text">
          <string>TextLabel</string>
         </property>
         <property name="alignment">
          <set>Qt::AlignCenter</set>
         </property>
        </widget>
       </item>
       <item row="2" column="0">
        <widget class="QLabel" name="averageSpeed">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Ignored" vsizetype="Ignored">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="font">
          <font>
           <family>Microsoft Sans Serif</family>
           <pointsize>20</pointsize>
          </font>
         </property>
         <property name="styleSheet">
          <string notr="true">color: rgb(100, 102, 105);
</string>
         </property>
         <property name="text">
          <string>TextLabel</string>
         </property>
         <property name="alignment">
          <set>Qt::AlignCenter</set>
         </property>
        </widget>
       </item>
      </layout>
     </widget>
    </widget>
    <widget class="QWidget" name="End_page">
     <widget class="QLabel" name="labelSpeed">
      <property name="geometry">
       <rect>
        <x>80</x>
        <y>80</y>
        <width>280</width>
        <height>91</height>
       </rect>
      </property>
      <property name="sizePolicy">
       <sizepolicy hsizetype="Ignored" vsizetype="Ignored">
        <horstretch>0</horstretch>
        <verstretch>0</verstretch>
       </sizepolicy>
      </property>
      <property name="font">
       <font>
        <family>Microsoft Sans Serif</family>
        <pointsize>20</pointsize>
       </font>
      </property>
      <property name="styleSheet">
       <string notr="true">color: rgb(100, 102, 105);
</string>
      </property>
      <property name="text">
       <string>TextLabel</string>
      </property>
     </widget>
     <widget class="QLabel" name="labelAccuracy">
      <property name="geometry">
       <rect>
        <x>440</x>
        <y>80</y>
        <width>280</width>
        <height>91</height>
       </rect>
      </property>
      <property name="font">
       <font>
        <family>Microsoft Sans Serif</family>
        <pointsize>20</pointsize>
       </font>
      </property>
      <property name="styleSheet">
       <string notr="true">color: rgb(100, 102, 105);
</string>
      </property>
      <property name="text">
       <string>TextLabel</string>
      </property>
     </widget>
     <widget class="QLabel" name="labelTime">
      <property name="geometry">
       <rect>
        <x>800</x>
        <y>80</y>
        <width>280</width>
        <height>91</height>
       </rect>
      </property>
      <property name="font">
       <font>
        <family>Microsoft Sans Serif</family>
        <pointsize>20</pointsize>
       </font>
      </property>
      <property name="styleSheet">
       <string notr="true">color: rgb(100, 102, 105);
</string>
      </property>
      <property name="text">
       <string>TextLabel</string>
      </property>
     </widget>
     <widget class="QPushButton" name="Button_Restart">
      <property name="geometry">
       <rect>
        <x>400</x>
        <y>240</y>
        <width>300</width>
        <height>90</height>
       </rect>
      </property>
      <property name="sizePolicy">
       <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
        <horstretch>0</horstretch>
        <verstretch>0</verstretch>
       </sizepolicy>
      </property>
      <property name="baseSize">
       <size>
        <width>0</width>
        <height>0</height>
       </size>
      </property>
      <property name="font">
       <font>
        <family>Microsoft Sans Serif</family>
        <pointsize>30</pointsize>
       </font>
      </property>
      <property name="styleSheet">
       <string notr="true">color: rgb(100, 102, 105);
</string>
      </property>
      <property name="inputMethodHints">
       <set>Qt::ImhNone</set>
      </property>
      <property name="text">
       <string>Начать заново</string>
      </property>
      <property name="autoDefault">
       <bool>false</bool>
      </property>
      <property name="default">
       <bool>false</bool>
      </property>
      <property name="flat">
       <bool>false</bool>
      </property>
     </widget>
    </widget>
   </widget>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""

class MainWindow(QMainWindow): 
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        # uic.loadUi('typing_1.0.ui', self)
        self.connection = sqlite3.connect('userStat.db')
        self.cursor = self.connection.cursor()
        self.lineEditPractice.textEdited.connect(self.startPractice)
        self.lineEditTraining.textEdited.connect(self.startTraining)
        self.setupUi()

    def setupUi(self):
        self.Button_Training.clicked.connect(self.btn_clicked)
        self.Button_Practice.clicked.connect(self.btn_clicked)
        self.Button_Profile.clicked.connect(self.btn_clicked)
        self.Button_Restart.clicked.connect(self.btn_clicked)
        self.Button_Quote.clicked.connect(self.btn_clicked)
        self.Button_Words.clicked.connect(self.btn_clicked)
        self.Button_ClearInfo.clicked.connect(self.clear_db)

        self.level_1.clicked.connect(self.lvl_select)
        self.level_2.clicked.connect(self.lvl_select)
        self.level_3.clicked.connect(self.lvl_select)
        self.level_4.clicked.connect(self.lvl_select)
        self.level_5.clicked.connect(self.lvl_select)
        self.level_6.clicked.connect(self.lvl_select)
        self.level_7.clicked.connect(self.lvl_select)
        self.level_8.clicked.connect(self.lvl_select)
        self.level_9.clicked.connect(self.lvl_select)
        self.level_10.clicked.connect(self.lvl_select)
        self.level_11.clicked.connect(self.lvl_select)
        self.level_12.clicked.connect(self.lvl_select)
        self.level_13.clicked.connect(self.lvl_select)
        self.level_14.clicked.connect(self.lvl_select)
        self.level_15.clicked.connect(self.lvl_select)
        
        self.navigation = {
            "Button_Practice": 0,
            "Button_Training": 2,
            "Button_Profile": 3,
            "Button_Restart": 4
        }

        self.modes = {
            "Practice": self.Button_Practice,
            "Training": self.Button_Training
        }

        self.Button_Profile.click()

    def clear_db(self):
        self.cursor.execute('drop table if exists UserInf')
        self.connection.commit()
        self.Button_Profile.click()

    def lvl_select(self):
        self.creationTrainingText(self.sender().objectName())
        self.stackedWidget.setCurrentIndex(1)

    def btn_clicked(self):
        self.buttons = self.sender().objectName()
        if self.buttons == "Button_Practice":
            self.creationPracticeText()
            self.stackedWidget.setCurrentIndex(self.navigation[self.buttons])
            self.lineEditPractice.clear()
            self.textBrowserPracticeEdit.clear()
            self.lineEditPractice.setEnabled(True)
            self.lineEditPractice.setFocus()
            self.mode = "Practice"
        
        elif self.buttons == "Button_Quote":
            self.creationPracticeText(quote=True)
            self.lineEditPractice.clear()
            self.textBrowserPracticeEdit.clear()
            self.lineEditPractice.setEnabled(True)
            self.lineEditPractice.setFocus()

        elif self.buttons == "Button_Words":
            self.creationPracticeText(quote=False)
            self.lineEditPractice.clear()
            self.textBrowserPracticeEdit.clear()
            self.lineEditPractice.setEnabled(True)
            self.lineEditPractice.setFocus()

        elif self.buttons == "Button_Training":
            self.stackedWidget.setCurrentIndex(self.navigation[self.buttons])
            self.textBrowserTrainingEdit.clear()
            self.lineEditTraining.clear()
            self.lineEditTraining.setEnabled(True)
            self.mode = "Training"

        elif self.buttons == "Button_Profile":
            self.stackedWidget.setCurrentIndex(self.navigation[self.buttons])

            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS UserInf (
            id INTEGER PRIMARY KEY,
            typing_speed INTEGER,
            time INTEGER,
            accuracy INTEGER
            )
            ''')
            if (self.cursor.execute('SELECT * FROM UserInf').fetchall()):
                completed_tests = self.cursor.execute('SELECT COUNT(*) FROM UserInf').fetchall()[0][0]
                avg_speed = self.cursor.execute('SELECT AVG(typing_speed) FROM UserInf').fetchall()[0][0]
                time_playing = self.cursor.execute('SELECT SUM(time) FROM UserInf').fetchall()[0][0]
                max_speed = self.cursor.execute('SELECT MAX(typing_speed) FROM UserInf').fetchall()[0][0]
                avg_acc = self.cursor.execute('SELECT AVG(accuracy) FROM UserInf').fetchall()[0][0]

                self.countCompletedTests.setText(f"Выполнено тестов: {completed_tests}")
                self.averageSpeed.setText(f"Средняя скорость: {round(avg_speed, 2)} ЗВМ")
                self.timeTyping.setText(f"Время печати: {time.strftime('%H:%M:%S', time.gmtime(time_playing))}")
                self.maxSpeed.setText(f"Максимальная скорость: {round(max_speed, 2)} ЗВМ")
                self.accuracy.setText(f"Средняя точность: {round(avg_acc, 2)} %")
                return
            
            self.countCompletedTests.setText(f"Выполнено тестов: {0}")
            self.averageSpeed.setText(f"Средняя скорость: {0} ЗВМ")
            self.timeTyping.setText(f"Время печати: 00:00:00")
            self.maxSpeed.setText(f"Максимальная скорость: {0} ЗВМ")
            self.accuracy.setText(f"Средняя точность: {0} %")

        elif self.buttons == "Button_Restart":
            self.modes[self.mode].click()

    def creationPracticeText(self, quote=False):
        text = list()
        if quote:
            text.extend((random.choice(word_level_list.practice_quotes)).split())
        else:
            for _ in range(20):
                text.append(random.choice(word_level_list.practice_text))

        self.ListWords = text
        self.textBrowserPracticeSolid.setText(" ".join(self.ListWords))
        self.isTestStarted = False

    def startPractice(self):
        lineText = self.lineEditPractice.text()
        browserText = self.ListWords[0]
        if not(self.isTestStarted):
            self.startTime = time.time()
            self.incorrectWords = 0
            self.countWords = len(self.ListWords)
            self.countCharacters = 1
            self.isTestStarted = True
            return

        if not(lineText):
            return 
        
        if lineText[-1] == " ":
            if lineText[:-1] == browserText:
                self.textBrowserPracticeEdit.insertHtml(f"<span style='color:rgb(152,152,146)'>{browserText} <\span>")
            else:
                self.textBrowserPracticeEdit.insertHtml(f"<span style='color:rgb(128,62,70)'>{browserText} <\span>")
                self.incorrectWords += 1
        
            self.ListWords = self.ListWords[1:]
            self.countCharacters += len(self.lineEditPractice.text())
            self.lineEditPractice.clear()

        if not(self.ListWords):
            resultTtime = time.time() - self.startTime
            accuracy = round(((self.countWords - self.incorrectWords) / self.countWords), 2) * 100
            self.lineEditPractice.setEnabled(False)
            self.cursor.execute('INSERT INTO UserInf (typing_speed, time, accuracy) VALUES (?, ?, ?)', (round((self.countCharacters / resultTtime * 60), 2), resultTtime, accuracy))
            self.connection.commit()
            self.stackedWidget.setCurrentIndex(self.navigation["Button_Restart"])
            self.labelSpeed.setText(f"Скорость: {round((self.countCharacters / resultTtime * 60), 2)} ЗВМ")
            self.labelAccuracy.setText(f"Точность: {round(accuracy, 2)} %")
            self.labelTime.setText(f"Время: {time.strftime('%H:%M:%S', time.gmtime(resultTtime))}")
            return
        
    def creationTrainingText(self, lvl, index=0):  
        if not(index):
            self.textPrime = word_level_list.levels[lvl]
            self.levelLen = len(self.textPrime)
            self.isTestStarted = False
        self.levelText = self.textPrime[index].split()
        self.textBrowserTrainingSolid.setText(" ".join(self.levelText))
        self.lineEditTraining.setFocus()

    def startTraining(self):
        lineText = self.lineEditTraining.text()
        browserText = self.levelText[0]
        if not(self.isTestStarted):
            self.startTime = time.time()
            self.incorrectWords = 0
            self.countWords = 0
            self.countCharacters = 1
            self.isTestStarted = True
            self.index = 0
            return

        if not(lineText):
            return 
        
        if lineText[-1] == " ":
            if lineText[:-1] == browserText:
                self.textBrowserTrainingEdit.insertHtml(f"<span style='color:rgb(152,152,146)'>{browserText} <\span>")
            else:
                self.textBrowserTrainingEdit.insertHtml(f"<span style='color:rgb(128,62,70)'>{browserText} <\span>")
                self.incorrectWords += 1

            self.countWords += 1
            self.levelText = self.levelText[1:]
            self.countCharacters += len(self.lineEditTraining.text())
            self.lineEditTraining.clear()

        if not(self.levelText):
            self.index += 1
            if self.index < self.levelLen:
                self.textBrowserTrainingEdit.clear()
                self.creationTrainingText(self, index=self.index)
                return
            
            resultTtime = time.time() - self.startTime
            accuracy = round(((self.countWords - self.incorrectWords) / self.countWords), 2) * 100
            self.lineEditTraining.setEnabled(False)
            self.cursor.execute('INSERT INTO UserInf (typing_speed, time, accuracy) VALUES (?, ?, ?)', (round((self.countCharacters / resultTtime * 60), 2), resultTtime, accuracy))
            self.connection.commit()
            self.stackedWidget.setCurrentIndex(self.navigation["Button_Restart"])
            self.labelSpeed.setText(f"Скорость: {round((self.countCharacters / resultTtime * 60), 2)} ЗВМ")
            self.labelAccuracy.setText(f"Точность: {round(accuracy, 2)} %")
            self.labelTime.setText(f"Время: {time.strftime('%H:%M:%S', time.gmtime(resultTtime))}")
            return


if __name__ == "__main__":
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
        
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())