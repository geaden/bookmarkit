/**
 * Spec files for Flash messages
 */

var flashMessage;
flashMessage = new FlashMessage();

function assertTrue(msg, expected) {
    if (!expected) {
        console.error('Assertion error: ' + msg);
    }
}

function runTests(e) {
    var $msgText = $('#msg-text > textarea').val();
    var $msgType = $('input[name="msgType"]:checked').val();
    var msgType = ($msgType) ? $msgType : 'info';
    flashMessage.show($msgText, $msgType, 'testFlashMessage');
    assertTrue(flashMessage.isShown);
}

//describe("FlashMessage", function() {
//  var flashMessage;
//
//  beforeEach(function() {
//    flashMessage = new FlashMessage();
//  });
//
//  it("should be shown with provided type", function() {
//    flashMessage.show('Foo', 'success', 'testFlashMessage');
//    expect(flashMessage.message).toEqual('Foo');
//    expect(flashMessage.type).toEqual('success');
//    expect(flashMessage.isShown).toEqual(true);
//  });
//
//  it("should be shown type info", function() {
//    flashMessage.show('Foo', 'noname', 'testFlashMessage');
//    expect(flashMessage.message).toEqual('Foo');
//    expect(flashMessage.type).toEqual('info');
//    expect(flashMessage.isShown).toEqual(true);
//  });
//
//  afterEach(function() {
//      $('#flashMessage').alert('close');
//  })

//  describe("when song has not listed type", function() {
//    beforeEach(function() {
//      flashMessage.show(song);
//      player.pause();
//    });
//
//    it("should indicate that the song is currently paused", function() {
//      expect(player.isPlaying).toBeFalsy();
//
//      // demonstrates use of 'not' with a custom matcher
//      expect(player).not.toBePlaying(song);
//    });
//
//    it("should be possible to resume", function() {
//      player.resume();
//      expect(player.isPlaying).toBeTruthy();
//      expect(player.currentlyPlayingSong).toEqual(song);
//    });
//  });
//
//  // demonstrates use of spies to intercept and test method calls
//  it("tells the current song if the user has made it a favorite", function() {
//    spyOn(song, 'persistFavoriteStatus');
//
//    player.play(song);
//    player.makeFavorite();
//
//    expect(song.persistFavoriteStatus).toHaveBeenCalledWith(true);
//  });
//
//  //demonstrates use of expected exceptions
//  describe("#resume", function() {
//    it("should throw an exception if song is already playing", function() {
//      player.play(song);
//
//      expect(function() {
//        player.resume();
//      }).toThrowError("song is already playing");
//    });
//  });
//});

