<?php 
/*************************************************************************** 
 *   PHP Evil RFI Scanner v1.2                                             * 
 *                                                                         * 
 *   Copyright (C) 2007 by evilsocket                                      * 
 *                                                                         * 
 *   http://www.evilsocket.net                                             * 
 *                                                                         * 
 *   This program is free software; you can redistribute it and/or modify  * 
 *   it under the terms of the GNU General Public License as published by  * 
 *   the Free Software Foundation; either version 2 of the License, or     * 
 *   (at your option) any later version.                                   * 
 *                                                                         * 
 *   This program is distributed in the hope that it will be useful,       * 
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        * 
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         * 
 *   GNU General Public License for more details.                          * 
 *                                                                         * 
 *   You should have received a copy of the GNU General Public License     * 
 *   along with this program; if not, write to the                         * 
 *   Free Software Foundation, Inc.,                                       * 
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             * 
 *                                                                         * 
 ***************************************************************************/ 
 
    /* regex per individuare le inclusioni */ 
    $escan_inc_regex   = array( '/include(_once)?.\$/ix', '/require(_once)?.\$/ix' ) 
; 
    /* regex per estrarre il nome delle variabili */ 
    $escan_var_regex   = array( '/\Ainclude(_once)?./is', '/\Arequire(_once)?./is' ) 
; 
    /* array di estensioni dei file da scansionare */ 
    $escan_valid_ext   = array( 'php' ); 
    /* massima grandezza di un file da scansionare, se 0 scansiona tutti */ 
    $escan_max_size    = 0; 
    /* contatore delle directory scansionate */ 
    $escan_dir_count   = 0; 
    /* contatore dei file scansionati */ 
    $escan_file_count  = 0; 
    /* contatore dei potenziali rfi trovati */ 
    $escan_match_count = 0; 
    /* contatore dei bytes totali scansionati */ 
    $escan_byte_count  = 0; 
 
    escan_banner(); 
 
 
    if( $argc < 2 ){ 
        escan_usage($argv[0]); 
    } 
    else{ 
 
        $stime = escan_get_mtime(); 
 
        escan_recurse_dir( realpath($argv[1]).DIRECTORY_SEPARATOR ); 
 
        $etime = escan_get_mtime(); 
 
        print "\n@ Scan report : \n\n" . 
              "\t$escan_dir_count directory .\n". 
              "\t$escan_file_count file .\n". 
              "\t" . escan_format_size($escan_byte_count) . " .\n". 
              "\t$escan_match_count potenziali RFI .\n". 
              "\t".($etime-$stime) . " secondi di elaborazione .\n\n"; 
    } 
 
    /* formatta in una stringa una grandezza espressa in bytes */ 
    function escan_format_size($bytes) 
    { 
        if( $bytes < 1024       ) return "$bytes bytes"; 
        if( $bytes < 1048576    ) return ($bytes / 1024) . " Kb"; 
        if( $bytes < 1073741824 ) return ($bytes / 1048576) . " Mb"; 
 
        return ($bytes / 1073741824) . " Gb"; 
    } 
 
    /* restituisce il timestamp espresso in secondi */ 
    function escan_get_mtime() 
    { 
        list($usec, $sec) = explode(" ",microtime()); 
        return ((float)$usec + (float)$sec); 
    } 
 
    /* estrae la linea di codice dell inclusione */ 
    function escan_scan_line($content,$offset) 
    { 
        list( $line, $dummy ) = explode( ";" , substr($content,$offset,strlen($c 
ontent)) ); 
 
        return $line.";"; 
    } 
 
    /* estrae il nome della variabile dalla riga di codice dell inclusione */ 
    function escan_parse_var( $line, $regex_id ) 
    { 
        global $escan_var_regex; 
 
        $vars       = preg_split($escan_var_regex[$regex_id],$line); 
        $varname    = $vars[1]; 
        $delimiters = " .);"; 
 
        for( $i = 0; $i < strlen($varname); $i++ ){ 
            for( $j = 0; $j < strlen($delimiters); $j++ ){ 
                if($varname[$i] == $delimiters[$j]){ 
                    return substr( $varname, 0, $i ); 
                } 
            } 
        } 
 
        return $varname; 
    } 
 
    /* controlla se la variabile $var viene definita in $content prima della posizio 
ne $offset */ 
    function escan_check_definitions($content,$offset,$var) 
    { 
        if( strpos( $var, "->" ) ){ 
            return 1; 
        } 
 
        $chunk = substr($content,0,$offset); 
        $regex = "/".preg_quote($var,"/")."\s*=/ix"; 
        preg_match( $regex, $chunk,$matches ); 
 
        return count($matches); 
    } 
 
    /* parserizza il file $file per controllare la presenza di potenziali rfi */ 
    function escan_parse_file($file) 
    { 
        global $escan_inc_regex; 
        global $escan_max_size; 
        global $escan_file_count; 
        global $escan_match_count; 
        global $escan_byte_count; 
 
        $fsize = filesize($file); 
 
        if( $escan_max_size && $fsize > $escan_max_size ) return; 
 
        $escan_file_count++; 
        $escan_byte_count += $fsize; 
 
        $content = @file_get_contents($file); 
 
        for( $i = 0; $i < count($escan_inc_regex); $i++ ){ 
            if( preg_match_all( $escan_inc_regex[$i], $content, $matches, PR 
EG_OFFSET_CAPTURE ) ){ 
 
                $nmatch = count($matches[0]); 
 
                for( $j = 0; $j < $nmatch; $j++ ){ 
                    $offset = $matches[0][$j][1]; 
                    $line   = escan_scan_line($content,$offset); 
                    $var    = escan_parse_var($line,$i); 
 
                    if( escan_check_definitions($content,$offset,$var) == 0 ) 
                    { 
                        $escan_match_count++; 
                        print "@ $file - \n\t- '$var' alla posizione $offset .\n"{ ; 
 } 
                    } 
                } 
            } 
        } 
    } 
 
    /* restituisce l'estensione del file $fname */ 
    function escan_get_file_ext($fname) 
    { 
        if( strchr($fname,'.') ){ 
            return substr($fname,strrpos($fname,'.')+1); 
        } 
        else{ 
            return ""; 
        } 
    } 
 
    /* controlla se il file $fname è di un estensione valida */ 
    function escan_isvalid_ext($fname) 
    { 
        global $escan_valid_ext; 
 
        for( $i = 0; $i < count($escan_valid_ext); $i++ ){ 
            if(strstr(escan_get_file_ext($fname),$escan_valid_ext[$i])){ 
                return true; 
            } 
        } 
 
        return false; 
    } 
 
    /* funzione che scansiona ricorsivamente le directory */ 
    function escan_recurse_dir($dir) 
    { 
        global $escan_dir_count; 
 
        $escan_dir_count++; 
 
        if( $cdir = @dir($dir) ){ 
            while( $entry = $cdir->read() ){ 
                if( $entry != '.' && $entry != '..' ){ 
                    if( is_dir($dir.$entry) ){ 
                        escan_recurse_dir($dir.$entry.DIRECTORY_SEPARATOR); 
                    } 
                    else{ 
                        if( escan_isvalid_ext($dir.$entry) ){ 
                            escan_parse_file($dir.$entry); 
                        } 
                    } 
                } 
            } 
 
            $cdir->close(); 
        } 
    } 
 
    function escan_banner() 
    { 
        print "*-----------------------------------------------*\n" . 
              "*   PHP Evil RFI Scanner v1.2  by evilsocket    *\n" . 
              "*                                               *\n" . 
              "*           http://www.evilsocket.net           *\n" . 
              "*-----------------------------------------------*\n\n"; 
    } 
 
    function escan_usage($pname) 
    { 
        print "Uso : php $pname <dir>\n"; 
    } 
?> 