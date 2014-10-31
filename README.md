MIDIParser
======================
MIDIParserはSMF(Standard MIDI File)形式の音楽データの構文解釈と音楽データの時間管理を行う[RT-Component][rtm]です．  
SMF形式の音楽ファイルを読み込み，音楽データが指定するタイミングでMIDI::MIDIMessage形式のデータを出力します．  
MIDI::Messageについては[こちら][idl]をごらんください．

[rtm]:http://www.openrtm.org/openrtm/ja
[idl]: https://github.com/HiroakiMatsuda/MIDIDataType

動作確認環境
------
Python:  
2.6.6  

OS:  
Windows 8/8.1 64bit / 32bit  

SMFの対応形式:   
フォーマットは0または1に対応しています．    
デルタタイムは絶対時間には対応していません．  

ファイル構成
------
MIDIParser  
│― idl   
│― MIDI  
│― MIDI\_POA  
│― midifile  
│　　　│― simpletest.mid  
│    
│― smf\_parser.py  
│― MIDIDataType\_idl.py  
│― MIDIParser.conf  
│― MIDIParser.py  

* MIDI, MIDI_POA, MIDIDataType.py  
独自データ型 MIDIDataTypeに関するファイルです．  

* smf\_parser.py  
MIDIファイルを解析するPython Moduleです．    
このモジュールの説明は、[こちら][smf_parser]をご覧ください．   

[smf_parser]: https://github.com/HiroakiMatsuda/smf_parser  
 
* MIDIParser.conf  
演奏する楽曲ファイルのファイルパスをコンフィグレーションを使用して記述できます．    

* MIDIParser.py  
MIDIParser RTC本体です．  

＊ 本RTCにおいてユーザーが操作すると想定しているファイルのみ説明しています．  

RTCの構成
------  
<img src="https://farm8.staticflickr.com/7561/15045826764_eec8cdac8a.jpg" width="400px" />    
データポートは1つあり、以下のようになっています  
  
* midi\_out port :OutPort  
データ型; MIDI::MIDIMessage  
SMFファイルから読み込んだMIDIメッセージを送信します．

* コンフィグレーション  
 ```midi_file ```  
 MIDIファイルのパスを以下のように指定します．  
 ```conf.mode<mode number>.midi_file: ./midifile/<file name>.mid ```  
 コンフィグレーションはActivate時に読み込みます．  
 曲を変更する場合は一度Deactivateを行い，再度Activateして下さい．


使い方：　MIDIConsoleOutを使用してテストする
------
###1. MIDIConsoleOutの入手する###
[MIDIConsoleOut][console]はMIDI::MIDIMessage型のデータを受け取り，コンソール上に表示するRTCです．  
[こちら][console]よりDLしてください．

[console]:http://pyserial.sourceforge.net/


###2. 解析するMIDIファイルを設定する###
MIDIParser RTCに解析させるMIDIファイルを設定します．  

MIDIParser.confをテキストエディタなどで開きます．  
以下のようにコンフィグレーションが設定されていると思います．  

```conf.mode0.midi_file: ./midifile/simpletest.mid ```     

以下のように，mode numberとfile nameを設定することで複数MIDIファイルを登録することができます．  
＊MIDIファイルはmidifileフォルダ内に配置することを前提としています．  

```conf.mode<mode number>.midi_file: ./midifile/<file name>.mid ```     
 
###3. MIDIConsoleOutの表示モードを設定する###
MIDIConsoleOutでは受け取ったMIDIメッセージの表示方法を変更することができます．  

MIDIConsoleOut.confをテクストエディタなどで開きます．  
以下のようにmode0がアクティブコンフィグレーションに設定されていると思います．  

```configuration.active_config: mode0```   

このmodeをmode0, mode1, mode2から選択することで表示方法を変えることができます．  
今回は，mode1を使用します．  
アクティブコンフィグレーションを以下のようにmode1に変更してください．  

```configuration.active_config: mode1```  
  
###4. MIDIメセージを受け取る###
MIDIParser RTCとMIDIConsoleOut RTCを実行してください．  
各RTCが起動したらMIDIParser RTCのmidi\_outポートとMIDIConsoleOut RTCのmidi\_inポートを接続します．  
各ポートを接続したらMIDIParser RTCをActivateします．  
すると，MIDIConsoleOut RTCのコンソール上に以下のようなメッセージが表示されると思います． 

<img src="https://farm8.staticflickr.com/7525/15480659597_7b957a5788.jpg" width="400px" />   

MIDIConsoleOut RTCのmode1ではNote OffとNote Onのメッセージ内容が表示されます．  
      
以上が本RTCの使い方となります．  

ライセンス
----------
Copyright &copy; 2014 Hiroaki Matsuda  
Licensed under the [Apache License, Version 2.0][Apache]  
Distributed under the [MIT License][mit].  
Dual licensed under the [MIT license][MIT] and [GPL license][GPL].  
 
[Apache]: http://www.apache.org/licenses/LICENSE-2.0
[MIT]: http://www.opensource.org/licenses/mit-license.php
[GPL]: http://www.gnu.org/licenses/gpl.html